from operator import itemgetter

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Group, Select, Row, Button
from aiogram_dialog.widgets.text import Format

from src.app.dialogs.user.trasnslate.getters import trasnlate_languages_getter
from src.app.dialogs.user.trasnslate.handlers import on_choose_translate_lang_to, on_auto_detect
from src.app.states.language import ChooseTranslateLanguagesSG

translate_languages = Dialog(
    Window(
        Format("{title}"),
        Row(
            Button(Format("{lang_from}"), id="lang_from"),
            Button(Format("{lang_to}"), id="lang_to")
        ),

        Group(
            Select(
                Format("{item[1]}"),
                id="tarnslate_lang",
                item_id_getter=itemgetter(0),
                items="buttons_list",
                on_click=on_choose_translate_lang_to
            ),
            width=2
        ),
        Button(Format("{auto}"), id="auto", on_click=on_auto_detect),
        state=ChooseTranslateLanguagesSG.choose_language,
        getter=trasnlate_languages_getter
    )
)
