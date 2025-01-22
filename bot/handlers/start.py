import loguru
from aiogram import Router, types
from aiogram.filters import CommandStart, Command, CommandObject

from models import TelegramUser
from keyboards.reply import reply_menu_keyboard

router = Router()


@router.message(CommandStart())
async def start_command_handler(
    message: types.Message,
    command: CommandObject,
):
    telegram_user, created = await TelegramUser.objects.aget_or_create(
        telegram_id=message.from_user.id,
        defaults={'username': message.from_user.username}
    )
    message_text = ''
    
    if created:
        message_text += f'Привет, {message.from_user.first_name}. '

    message_text += 'Выбери действие.'
    
    await message.answer(
        message_text,
        reply_markup=reply_menu_keyboard
    )
    
    
    

    
    

