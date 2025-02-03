import loguru
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext

from models import TelegramUser
from keyboards.reply import reply_russian_menu_keyboard

router = Router()

@router.message(CommandStart())
async def start_command_handler(
    message: types.Message,
    command: CommandObject,
    state: FSMContext,
):
    await state.clear()
    
    if not message.from_user.username:
        await message.answer(
            'Для старта работы бота, '
            'добавьте пожалуйста <b>username</b> в свой телеграм аккаунт.',
            parse_mode='HTML',
        )
        return
    
    telegram_user, created = (
        await TelegramUser.objects
        .aget_or_create_by_from_user(from_user=message.from_user)
    )
    message_text = ''
    
    if created:
        message_text += f'Привет, {message.from_user.first_name}. '

    message_text += 'Выбери действие.'
    
    await message.answer(
        message_text,
        reply_markup=reply_russian_menu_keyboard
    )
    
    
    

    
    

