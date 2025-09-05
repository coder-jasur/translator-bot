from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

back_to_admin_menu_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_admin_menu")
        ]
    ]
)