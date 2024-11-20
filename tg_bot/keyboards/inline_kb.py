from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON

def create_inline_keyboard(width: int, buttons: list[str]) -> InlineKeyboardMarkup:
    kb_builder =  InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button) for button in buttons], width=width)
    return kb_builder.as_markup()