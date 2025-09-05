import logging
from typing import Any

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from asyncpg import Connection

from src.app.keyboards.inline import back_to_admin_menu_keyboards
from src.app.services.broadcaster import Broadcaster
from src.app.states.broadcast import BroadcastingManagerSG

logger = logging.getLogger(__name__)


broadcater_router = Router()

async def start_broadcasting_manager(message: Message, state: FSMContext):
    await message.edit_text(
        "Для рассылки отправьте <b>сообщение</b>.",
        parse_mode="HTML"
    )
    await state.set_state(BroadcastingManagerSG.get_message)


@broadcater_router.message(BroadcastingManagerSG.get_message)
async def get_broadcasting_message(message: Message, state: FSMContext, **kwargs):
    if message.poll:
        await message.delete()
        return await message.answer(
            "❌ Неправильный формат!"
        )

    album = kwargs.get("album")
    if album:
        await state.update_data(album=album)
    else:
        await state.update_data(message=message)

    await state.set_state(BroadcastingManagerSG.confirm_broadcasting)
    await message.answer(
        "Вы уверены, что хотите начать рассылку?",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="❌ Отменить", callback_data="broadcast:cancel"),
                    InlineKeyboardButton(text="✅ Подтвердить", callback_data="broadcast:confirm"),
                ]
            ]
        )
    )


@broadcater_router.callback_query(BroadcastingManagerSG.confirm_broadcasting, F.data == "broadcast:cancel")
async def on_cancel_broadcast(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.edit_text("Рассылка отменена", reply_markup=back_to_admin_menu_keyboards)


@broadcater_router.callback_query(BroadcastingManagerSG.confirm_broadcasting, F.data == "broadcast:confirm")
async def on_confirm_broadcast(call: CallbackQuery, state: FSMContext, conn: Connection, bot: Bot) -> Any:
    try:
        data = await state.get_data()
        print(data)
        message = data.get("message")
        album = data.get("album")

        if not album and not message:
            raise ValueError("Сообщение для рассылки отсутствует!")

        await call.message.edit_text("Рассылка пользователям запущена...")
        broadcaster = Broadcaster(
            bot=bot,
            session=conn,
            admin_id=call.from_user.id,
            broadcasting_message=message,
            album=album,
            batch_size=5000  # размер пачки
        )

        # Запуск рассылки
        count_blocked, count_deleted, count_limited, count_deactivated = await broadcaster.broadcast()

        # Результаты рассылки
        result_message = "Рассылка завершена."

        if count_blocked:
            result_message += f"\nОбнаружено {count_blocked} пользователей, заблокировавших бота."

        if count_deleted:
            result_message += f"\nОбнаружено {count_deleted} удалённых аккаунтов."

        if count_limited:
            result_message += f"\nОбнаружено {count_limited} аккаунтов, ограниченных Telegram."

        if count_deactivated:
            result_message += f"\nОбнаружено {count_deactivated} деактивированных аккаунтов."

        if not count_blocked and not count_deleted and not count_limited and not count_deactivated:
            result_message += "\nВсе сообщения успешно доставлены."

        await call.message.edit_text(result_message)

    except ValueError as e:
        return await call.message.answer(f"Ошибка при рассылке: {e}")

    except Exception as e:
        logger.error(f"Ошибка при рассылке: {e}")
        return await call.message.answer(f"Ошибка при рассылке: {e}")