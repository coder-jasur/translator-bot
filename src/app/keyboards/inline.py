from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

back_to_admin_menu_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ orqaga", callback_data="back_to_admin_menu")
        ]
    ]
)