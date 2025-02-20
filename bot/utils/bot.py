from aiogram import Bot, types
from aiogram.exceptions import TelegramBadRequest
from django.conf import settings

from models import (
    TelegramUser,
    FeedBack,
    Question,
    PostTopicOffer,
    Event
) 
from loader import bot


async def edit_text_or_answer(
    message: types.Message,
    **kwargs,
):
    try:
        await message.edit_text(**kwargs)
    except TelegramBadRequest:
        await message.answer(**kwargs)
    
    
def get_manager_account_message(telegram_user: TelegramUser):
    manager_account = f'@{telegram_user.manager_account}' \
        if telegram_user.manager_account else 'нет'
        
    return manager_account


async def send_question_message_to_group(
    telegram_user: TelegramUser,
    question: Question,
):
    manager_account = get_manager_account_message(telegram_user) 
    await bot.send_message(
        text=(
            f'Пользователь @{telegram_user.username} '
            f'(ID: {telegram_user.telegram_id}) задал вопрос:\n' 
            f'<em><b>"{question.text}"</b></em>.\n\n'
            f'Менеджер: {manager_account}'
        ),
        chat_id=settings.CONTACT_GROUP_ID,
        parse_mode='HTML'
    )
    
    
async def send_feedback_message_to_group(
    telegram_user: TelegramUser,
    feedback: FeedBack,
):
    manager_account = get_manager_account_message(telegram_user)  
    await bot.send_message(
        text=(
            f'Пользователь @{telegram_user.username} '
            f'(ID: {telegram_user.telegram_id}) оставил обратную связь:\n' 
            f'<em><b>"{feedback.text}"</b></em>.\n\n'
            f'Менеджер: {manager_account}'
        ),
        chat_id=settings.CONTACT_GROUP_ID,
        parse_mode='HTML'
    )
    
    
async def send_post_topic_message_to_group(
    telegram_user: TelegramUser,
    post_topic: PostTopicOffer,
):
    manager_account = get_manager_account_message(telegram_user) 
    await bot.send_message(
        text=(
            f'Пользователь @{telegram_user.username} '
            f'(ID: {telegram_user.telegram_id}) предложил тему ' 
            f'<em><b>"{post_topic.text}"</b></em> для поста.'
        ),
        chat_id=settings.CONTACT_GROUP_ID,
        parse_mode='HTML'
    )


async def send_take_part_event_message_to_group(
    telegram_user: TelegramUser,
    event: Event,
):
    manager_account = get_manager_account_message(telegram_user)
    await bot.send_message(
        text=(
            f'Пользователь @{telegram_user.username} '
            f'(ID: {telegram_user.telegram_id}) '
            f'будет присутствовать на {event.name}\n\n'
            f'Менеджер: {manager_account}'
        ),
        chat_id=settings.CONTACT_GROUP_ID,
        parse_mode='HTML'
    )

