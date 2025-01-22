import loguru
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from django.conf import settings

from .state import (
    QuestionState,
    FeedBackState,
    PostTopicOfferState,
)
from models import (
    TelegramUser,
    PostFeedBackRequest,
    FeedBack,
    Question,
    PostTopicOffer
) 
from keyboards.reply import (
    reply_menu_keyboard,
    reply_cancel_keyboard
)


router = Router()


@router.message(
    StateFilter('*'),
    (F.text.casefold() == 'отмена ❌')
)
async def cancel_callback_handler(
    message: types.Message,
    state: FSMContext,
):
    await state.clear()
    await message.answer(
        'Действие отменено',
        reply_markup=reply_menu_keyboard,
    )


@router.message(F.text.casefold() == 'задать вопрос ❓')
async def ask_question_message_handler(
    message: types.Message,
    state: FSMContext,
):
    await message.answer(
        'Что вы хотели бы узнать?',
        reply_markup=reply_cancel_keyboard,
    )
    await state.set_state(QuestionState.text)
    
    
@router.message(F.text, QuestionState.text)
async def process_question_message_handler(
    message: types.Message,
    state: FSMContext,
):
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=message.from_user.id
    )
    await Question.objects.acreate(
        text=message.text,
        telegram_user=telegram_user,
    )
    await message.answer(
        'Спасибо за ваш вопрос!\n'
        'С вами скоро свяжется наш менеджер.',
        reply_markup=reply_menu_keyboard,
    )
    await state.clear()
    
    
@router.message(
    F.text.casefold() == 'оставить обратную связь 📤'
)
async def send_feedback_message_handler(
    message: types.Message,
    state: FSMContext,
):
    await message.answer(
        'Отправьте сообщение.\n\n'
        'Я запишу и передам его администрации канала.',
        reply_markup=reply_cancel_keyboard,
    )
    await state.set_state(FeedBackState.text)
    
    
@router.message(F.text, FeedBackState.text)
async def process_feedback_message_handler(
    message: types.Message,
    state: FSMContext,
):
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=message.from_user.id
    )
    await FeedBack.objects.acreate(
        text=message.text,
        telegram_user=telegram_user,
    )
    await message.answer(
        'Ваше сообщение принято.\n'
        'Спасибо за обратную связь!',
        reply_markup=reply_menu_keyboard,
    )
    await state.clear()
    
    
@router.message(
    F.text.casefold() == 'предложить тему поста 📝'
)
async def offer_post_topic_message_handler(
    message: types.Message,
    state: FSMContext,
):
    await message.answer(
        'Отправьте вашу тему для поста.',
        reply_markup=reply_cancel_keyboard,
    )
    await state.set_state(PostTopicOfferState.text)
    
    
@router.message(F.text, PostTopicOfferState.text)
async def process_post_topic_message_handler(
    message: types.Message,
    state: FSMContext,
):
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=message.from_user.id
    )
    await PostTopicOffer.objects.acreate(
        text=message.text,
        telegram_user=telegram_user,
    )
    await message.answer(
        'Ваше сообщение принято.\n'
        'Спасибо за обратную связь!',
        reply_markup=reply_menu_keyboard,
    )
    await state.clear()
    
    
    
@router.callback_query(F.data.startswith('contact_me_'))
async def contact_me_callback_handler(
    callback: types.CallbackQuery,
):
    telegram_user, _ = await TelegramUser.objects.aget_or_create(
        telegram_id=callback.from_user.id,
        defaults={'username': callback.from_user.username}
    )
    post_id = callback.data.split('_')[-1]
    post, created = await PostFeedBackRequest.objects.aget_or_create(
        post_id=post_id,
        telegram_user=telegram_user,
    )
    
    if not created:
        await callback.answer(
            'Вы уже отправили запрос. '
            'Ожидайте ответа менеджера.'
        )
        return
    
    await callback.answer(
        'Ваш запрос принят,'
        'скоро вам напишет ваш аккаунт-менеджер.'
    )
    post_link = f'{settings.CHANNEL_LINK}/{callback.message.message_id}'
    
    if telegram_user.manager_account:
        manager_account = f'@{telegram_user.manager_account}'
    else:
        manager_account = 'нет'
        
    await callback.bot.send_message(
        text=(
            f'Пользователь @{callback.from_user.username} хочет, '
            f'чтобы с ним связались по <a href="{post_link}">посту</a>\n\n'
            f'Менеджер: {manager_account}'
        ),
        chat_id=settings.CONTACT_GROUP_ID,
        parse_mode='HTML'
    )
    
    
    
