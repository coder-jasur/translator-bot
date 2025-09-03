from aiogram_dialog import DialogManager


async def start_menu_getter(dialog_manager: DialogManager, **_):
    return {"choose_language": "🇺🇿 Tilni tanlang\n\n🇷🇺 выберите язык\n\n🇺🇸 choose language"}