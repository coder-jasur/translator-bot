from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

back_to_admin_menu_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◄ Назад", callback_data="back_to_admin_menu")
        ]
    ]
)

def not_channels_button(channel_data):
    builder_button = InlineKeyboardBuilder()
    for channel in channel_data:

        builder_button.row(
            InlineKeyboardButton(text=channel[1], url=channel[6])
        )

    builder_button.row(InlineKeyboardButton(text="✅", callback_data="check_sub"))
    return builder_button.as_markup()