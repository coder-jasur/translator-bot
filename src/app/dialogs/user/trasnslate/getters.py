from pprint import pprint

from aiogram_dialog import DialogManager
from asyncpg import Connection

from src.app.database.queries.users import UserActions
from src.app.texts import texts


def make_languages(selected: str):
    langs = {
        "uz": "🇺🇿 O'zbekcha",
        "ru": "🇷🇺 Русский",
        "en": "🇺🇸 English",
        "fr": "🇫🇷 French",
        "es": "🇪🇸 Español",
        "ar": "🇸🇦 Arab",
        "it": "🇮🇹 Italiano",
        "jp": "🇯🇵 Japanese",
        "kr": "🇰🇷 Korean",
        "zh-TW": "🇨🇳 Chinese"

    }

    return [
        (code, name + (" ✅" if code == selected else ""))
        for code, name in langs.items()
    ]

def make_languages_to(selected: str):
    langs = {
        "uz": "🇺🇿 O'zbekcha",
        "ru": "🇷🇺 Русский",
        "en": "🇺🇸 English",
        "fr": "🇫🇷 French",
        "es": "🇪🇸 Español",
        "ar": "🇸🇦 Arabic",
        "it": "🇮🇹 Italiano",
        "ja": "🇯🇵 Japanese",
        "ko": "🇰🇷 Korean",
        "zh-TW": "🇨🇳 Chinese"
    }

    return [
        (code + " lang to", name + (" ✅" if code == selected else ""))
        for code, name in langs.items()
    ]



async def trasnlate_languages_getter(dialog_manager: DialogManager, **_):
    conn: Connection = dialog_manager.middleware_data["conn"]
    user_actions = UserActions(conn)
    user_data = await user_actions.get_user(dialog_manager.event.from_user.id)

    lang_to = user_data[4]
    lang_from = user_data[5]

    if dialog_manager.start_data:
        lang = dialog_manager.start_data
    else:
        lang = dialog_manager.middleware_data["lang"]

    text = texts["start"][lang]

    from_langs = make_languages(lang_from)
    to_langs = make_languages_to(lang_to)

    buttons = []
    for from_item, to_item in zip(from_langs, reversed(to_langs)):
        buttons.append(from_item)
        buttons.append(to_item)


    return {
        "title": text,
        "buttons_list": buttons,
        "lang_from": texts["lang_ariented_text"]["lang_from"][lang],
        "lang_to": texts["lang_ariented_text"]["lang_to"][lang],
        "auto": texts["auto_detect"][lang] + " ✅" if user_data[5] == "auto" else texts["auto_detect"][lang]
    }