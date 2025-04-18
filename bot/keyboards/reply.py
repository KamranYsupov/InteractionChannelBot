﻿from typing import Sequence
from datetime import datetime

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from django.utils import timezone


def get_reply_keyboard(
    buttons: Sequence[str],
    resize_keyboard: bool = True,
) -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=button_text)] for button_text in buttons]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=resize_keyboard
    )
    
def get_reply_contact_keyboard(
    text: str = 'Отправить номер телефона 📲'
) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=text, request_contact=True)],
        [KeyboardButton(text='Отмена ❌')]
    ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    
    
reply_russian_cancel_keyboard = get_reply_keyboard(buttons=('Отмена ❌',))
reply_english_cancel_keyboard = get_reply_keyboard(buttons=('Cancel ❌',))

reply_russian_menu_keyboard = get_reply_keyboard(
    buttons=(
        'Задать вопрос ❓',
        'Оставить обратную связь 📤',
        'Посмотреть календарь мероприятий 📅',
        'Предложить тему поста 📝',
        'Change language 🇺🇸',
    )
)
reply_english_menu_keyboard = get_reply_keyboard(
    buttons=(
        'Ask a question ❓',
        'Leave feedback 📤',
        'View the event calendar 📅',
        'Suggest a post topic 📝',
        'Изменить язык 🇷🇺',
    )
)
reply_keyboard_remove = ReplyKeyboardRemove()
reply_contact_keyboard = get_reply_contact_keyboard()

    
