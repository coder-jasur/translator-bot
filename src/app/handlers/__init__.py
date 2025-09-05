from aiogram import Dispatcher, Router, F

from src.app.dialogs import dialog_register
from src.app.dialogs.admin.handlers import broadcater_router
from src.app.handlers.admin_commands import admin_commands_router
from src.app.handlers.language import language_router
from src.app.handlers.start import start_router
from src.app.handlers.translate import translate_router


def register_all_routers(dp: Dispatcher, admins: list):
    main_router = Router()
    registrar_admin_routers(main_router, admins)
    dialog_register(dp)
    main_router.include_router(broadcater_router)
    main_router.include_router(start_router)
    main_router.include_router(language_router)

    main_router.include_router(translate_router)
    dp.include_router(main_router)


def registrar_admin_routers(router: Router, admins: list):
    admins_id = []
    for admin in admins:
        admins_id.append(int(admin))
    admin_router = Router()
    admin_router.message.filter(F.from_user.id.in_(admins_id))
    admin_router.callback_query.filter(F.from_user.id.in_(admins_id))

    admin_router.include_router(admin_commands_router)
    router.include_router(admin_router)
