from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Group, Button
from aiogram_dialog.widgets.text import Format, Const

from src.app.dialogs.user.language.getters import start_menu_getter
from src.app.dialogs.user.language.handlers import on_choose_language
from src.app.states.language import ChooseLanguageSG

choose_language_dialog = Dialog(
    Window(
        Format("{choose_language}"),
        Group(
            Button(text=Const("🇺🇿 O'zbekcha"), id="uz", on_click=on_choose_language),
            Button(text=Const("🇷🇺 Русский"), id="ru", on_click=on_choose_language),
            Button(text=Const("🇺🇸 English"), id="en", on_click=on_choose_language),
        ),
        state=ChooseLanguageSG.choose_language,
        getter=start_menu_getter
    ),

)
