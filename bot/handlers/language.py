import loguru
from aiogram import Router, types, F
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from django.conf import settings

from models import (
    TelegramUser,
    Event
) 
from keyboards.reply import (
    reply_russian_menu_keyboard,
    reply_english_menu_keyboard
)

router = Router()

@router.message(
    or_f(
        F.text.casefold() == 'change language 🇺🇸',
        F.text.casefold() == 'изменить язык 🇷🇺',
    )
)
async def change_language_handler(
    message: types.Message,
):
    if message.text.casefold() == 'change language 🇺🇸':
        message_data = {
            'text': 'Language has changed ✅',
            'reply_markup': reply_english_menu_keyboard,
        }
    else:
        message_data = {
            'text': 'Язык изменён ✅',
            'reply_markup': reply_russian_menu_keyboard,
        }
    
        
        
    await message.answer(**message_data)
    