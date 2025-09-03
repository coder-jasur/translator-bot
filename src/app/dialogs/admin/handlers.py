import logging

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
)
from aiogram_dialog import DialogManager, StartMode, Window, Dialog, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Start
from aiogram_dialog.widgets.text import Const, Case
from asyncpg import Connection

from src.app.database.queries.users import UserActions
from src.app.services.broadcaster import Broadcaster
from src.app.states.admin import AdminStateSG
from src.app.states.broadcast import BroadcasterSG

logger = logging.getLogger(__name__)

broadcater_router = Router()


async def users_count_getter(dialog_manager: DialogManager, **_):
    conn: Connection = dialog_manager.middleware_data["conn"]

    user_actions = UserActions(conn)
    all_users = await user_actions.get_all_user()

    return {"users_count": f"количества пользывателей: {len(all_users)}"}




async def delete_preview_message(
        call: CallbackQuery,
        manager: DialogManager
) -> None:
    ctx = manager.dialog_data
    bot: Bot = manager.middleware_data["bot"]
    try:
        if ctx.get("broadcasting_message"):
            message = Message.model_validate(ctx["broadcasting_message"])
            await bot.delete_message(call.from_user.id, message_id=message.message_id)
    except Exception as e:
        logging.exception(e)


async def on_creative_input(
        message: Message,
        _message_input: MessageInput,
        manager: DialogManager
) -> None:
    ctx = manager.dialog_data
    album = manager.middleware_data.get("album")
    if album:
        ctx["album"] = [
            message.model_dump(mode="json", exclude_defaults=True)
            for message in album
        ]
    else:
        ctx["creative"] = message.model_dump(mode="json", exclude_defaults=True)
    await manager.switch_to(BroadcasterSG.confirm_broadcasting, show_mode=ShowMode.DELETE_AND_SEND)


async def on_publish(
        call: CallbackQuery,
        _button: Button,
        manager: DialogManager
) -> Message:
    """
    Обработчик запуска рассылки сообщений пользователям.

    Args:
        call: Объект колбэка от нажатия на кнопку
        _button: Объект кнопки, которая была нажата
        manager: Менеджер диалога, содержащий данные и middleware
    """
    try:
        ctx = manager.dialog_data
        manager.show_mode = ShowMode.DELETE_AND_SEND
        session: Connection = manager.middleware_data["conn"]
        bot: Bot = manager.middleware_data["bot"]

        await call.message.delete()

        if not session or not bot:
            return await call.message.answer("Ошибка: не удалось получить сессию или бота")

        # Обработка одиночного сообщения
        message = None
        if ctx.get("creative"):
            try:
                message = Message.model_validate(ctx["creative"])
            except Exception as e:
                logging.error(f"Ошибка валидации сообщения: {e}")
                return await call.message.answer(
                    f"Ошибка подготовки сообщения для рассылки: {e}"
                )

        # Обработка альбома сообщений
        album = None
        if manager.dialog_data.get("album"):
            try:
                album = [
                    Message.model_validate(msg_data) for msg_data in ctx["album"]
                    if msg_data  # Проверка на None
                ]
                # Проверка, что альбом не пустой после валидации
                if not album:
                    return await call.message.answer(
                        "Ошибка: альбом пуст или содержит некорректные сообщения"
                    )

            except Exception as e:
                logging.error(f"Ошибка валидации альбома: {e}")
                return await call.message.answer(
                    f"Ошибка подготовки альбома для рассылки: {e}"
                )

        # Проверка наличия контента для рассылки
        if not message and not album:
            return await call.message.answer(
                "Ошибка: нет сообщения или альбома для рассылки"
            )

        # Создание и запуск broadcaster, используя рассылку пачками
        try:
            # Вывод информации о запуске рассылки
            await call.message.answer("Начинаем рассылку пользователям...")

            broadcaster = Broadcaster(
                bot=bot,
                conn=session,
                admin_id=call.from_user.id,
                broadcasting_message=message,
                album=album,
                batch_size=5000  # Устанавливаем размер пачки
            )

            # Запуск рассылки
            count_blocked, count_deleted, count_limited, count_deactivated = await broadcaster.broadcast()

            # Вывод результатов рассылки
            result_message = "Рассылка завершена."

            if count_blocked:
                result_message += (
                    f"\nОбнаружено {count_blocked} заблокировавших бота."
                )

            if count_deleted:
                result_message += (
                    f"\nОбнаружено {count_deleted} аккаунтов, которые были удалены."
                )

            if count_limited:
                result_message += (
                    f"\nОбнаружено {count_limited} аккаунтов, которые ограничены тг."
                )

            if count_deactivated:
                result_message += (
                    f"\nОбнаружено {count_deleted} аккаунтов, которые деактивированы."
                )

            if not count_blocked and not count_deleted and not count_limited and not count_deactivated:
                result_message += "\nВсе сообщения доставлены успешно."

            await call.message.answer(result_message)

        except ValueError as e:
            # Обработка ошибок валидации в Broadcaster
            return await call.message.answer(f"Ошибка конфигурации рассылки: {e}")

        except Exception as e:
            logging.error(f"Ошибка при выполнении рассылки: {e}")
            return await call.message.answer(f"Ошибка при выполнении рассылки: {e}")

    except Exception as e:
        # Глобальный обработчик исключений
        logging.error(f"Необработанная ошибка в on_publish: {e}")
        return await call.message.answer(
            "Произошла непредвиденная ошибка при запуске рассылки"
        )

    finally:
        await manager.start(AdminStateSG.menu, mode=StartMode.RESET_STACK)


async def on_broadcast_to_users_with_subscription(_, __, manager: DialogManager):
    manager.current_context().dialog_data |= {"has_mail": True}
    await manager.switch_to(BroadcasterSG.get_creative)


async def on_broadcast_to_users_without_subscription(_, __, manager: DialogManager):
    ctx = manager.dialog_data
    ctx |= {"has_mail": False}
    await manager.switch_to(BroadcasterSG.get_creative)


async def on_cancel_broadcasting(call: CallbackQuery, __, manager: DialogManager):
    await delete_preview_message(call, manager)


async def get_msg_type(dialog_manager: DialogManager, **_kwargs):
    ctx = dialog_manager.dialog_data
    return {"msg_type": ctx.get("msg_type", "get_creative")}


broadcaster_dialog = Dialog(
    Window(
        Case(
            {
                "get_creative": Const("Отправьте сообщение для рассылки"),
                "incorrect_creative_type": Const("Неправильный формат! Пожалуйста попробуйте заново.")
            },
            selector="msg_type"
        ),
        Start(Const("✕ Отменить"), id="back", state=AdminStateSG.menu, mode=StartMode.RESET_STACK),
        MessageInput(func=on_creative_input),
        state=BroadcasterSG.get_creative,
        getter=get_msg_type
    ),
    Window(
        Const(
            "<b>Подтвердите запуск рассылки или отмените её.</b> "
            "Больше предупреждений не будет!"
        ),
        Button(Const("Запустить рассылку"), id="publish", on_click=on_publish),
        Start(
            Const("✕ Отменить"),
            id="cancel",
            state=AdminStateSG.menu,
            on_click=on_cancel_broadcasting,
            mode=StartMode.RESET_STACK,
        ),
        state=BroadcasterSG.confirm_broadcasting
    )
)