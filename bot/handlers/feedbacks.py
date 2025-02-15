import loguru
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from django.conf import settings

from .state import (
    RuQuestionState,
    RuFeedBackState,
    RuPostTopicOfferState,
    EnQuestionState,
    EnFeedBackState,
    EnPostTopicOfferState,
)
from models import (
    TelegramUser,
    PostFeedBackRequest,
    FeedBack,
    Question,
    PostTopicOffer
)
from keyboards.reply import (
    reply_russian_menu_keyboard,
    reply_russian_cancel_keyboard,
    reply_english_menu_keyboard,
    reply_english_cancel_keyboard,
)
from utils.bot import (
    send_question_message_to_group,
    send_feedback_message_to_group,
    send_post_topic_message_to_group,
)

router = Router()


@router.message(
    StateFilter('*'),
    (F.text.casefold() == 'отмена ❌'),
)
async def cancel_callback_handler(
        message: types.Message,
        state: FSMContext,
):
    await state.clear()
    await message.answer(
        'Действие отменено',
        reply_markup=reply_russian_menu_keyboard,
    )


@router.message(F.text.casefold() == 'задать вопрос ❓')
async def ask_question_message_handler(
        message: types.Message,
        state: FSMContext,
):
    await message.answer(
        'Что вы хотели бы узнать?',
        reply_markup=reply_russian_cancel_keyboard,
    )
    await state.set_state(RuQuestionState.text)


@router.message(F.text, RuQuestionState.text)
async def process_question_message_handler(
        message: types.Message,
        state: FSMContext,
):
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=message.from_user.id
    )
    question = await Question.objects.acreate(
        text=message.text,
        telegram_user=telegram_user,
    )
    await message.answer(
        'Спасибо за ваш вопрос!\n'
        'С вами скоро свяжется наш менеджер.',
        reply_markup=reply_russian_menu_keyboard,
    )
    await send_question_message_to_group(
        telegram_user=telegram_user,
        question=question
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
        reply_markup=reply_russian_cancel_keyboard,
    )
    await state.set_state(RuFeedBackState.text)


@router.message(F.text, RuFeedBackState.text)
async def process_feedback_message_handler(
        message: types.Message,
        state: FSMContext,
):
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=message.from_user.id
    )
    feedback = await FeedBack.objects.acreate(
        text=message.text,
        telegram_user=telegram_user,
    )
    await message.answer(
        'Ваше сообщение принято.\n'
        'Спасибо за обратную связь!',
        reply_markup=reply_russian_menu_keyboard,
    )
    await send_feedback_message_to_group(
        telegram_user=telegram_user,
        feedback=feedback
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
        reply_markup=reply_russian_cancel_keyboard,
    )
    await state.set_state(RuPostTopicOfferState.text)


@router.message(F.text, RuPostTopicOfferState.text)
async def process_post_topic_message_handler(
        message: types.Message,
        state: FSMContext,
):
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=message.from_user.id
    )
    post_topic = await PostTopicOffer.objects.acreate(
        text=message.text,
        telegram_user=telegram_user,
    )
    await message.answer(
        'Ваше сообщение принято.\n'
        'Спасибо за обратную связь!',
        reply_markup=reply_russian_menu_keyboard,
    )
    await send_post_topic_message_to_group(
        telegram_user=telegram_user,
        post_topic=post_topic
    )
    await state.clear()


@router.message(
    StateFilter('*'),
    (F.text.casefold() == 'cancel ❌')
)
async def en_cancel_callback_handler(
        message: types.Message,
        state: FSMContext,
):
    await state.clear()
    await message.answer(
        'Action canceled',
        reply_markup=reply_english_menu_keyboard,
    )


@router.message(F.text.casefold() == 'ask a question ❓')
async def ask_question_message_handler(
        message: types.Message,
        state: FSMContext,
):
    await message.answer(
        'What would you like to know?',
        reply_markup=reply_english_cancel_keyboard,
    )
    await state.set_state(EnQuestionState.text)


@router.message(F.text, EnQuestionState.text)
async def process_question_message_handler(
        message: types.Message,
        state: FSMContext,
):
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=message.from_user.id
    )
    question = await Question.objects.acreate(
        text=message.text,
        telegram_user=telegram_user,
    )
    await message.answer(
        'Thanks for your question!\n'
        'Our manager will contact you soon.',
        reply_markup=reply_english_menu_keyboard,
    )
    await send_question_message_to_group(
        telegram_user=telegram_user,
        question=question
    )
    await state.clear()


@router.message(
    F.text.casefold() == 'leave a feedback 📤'
)
async def send_feedback_message_handler(
        message: types.Message,
        state: FSMContext,
):
    await message.answer(
        'Send a message.\n\n'
        "I'll jot it down and pass it to the channel administration.",
        reply_markup=reply_english_cancel_keyboard,
    )
    await state.set_state(EnFeedBackState.text)


@router.message(F.text, EnFeedBackState.text)
async def process_feedback_message_handler(
        message: types.Message,
        state: FSMContext,
):
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=message.from_user.id
    )
    feedback = await FeedBack.objects.acreate(
        text=message.text,
        telegram_user=telegram_user,
    )
    await message.answer(
        'Your message is accepted.\n'
        'Thank you for the feedback!',
        reply_markup=reply_english_menu_keyboard,
    )
    await send_feedback_message_to_group(
        telegram_user=telegram_user,
        feedback=feedback
    )
    await state.clear()


@router.message(
    F.text.casefold() == 'offer a post topic 📝'
)
async def offer_post_topic_message_handler(
        message: types.Message,
        state: FSMContext,
):
    await message.answer(
        'Send your post topic.',
        reply_markup=reply_english_cancel_keyboard,
    )
    await state.set_state(EnPostTopicOfferState.text)


@router.message(F.text, EnPostTopicOfferState.text)
async def process_post_topic_message_handler(
        message: types.Message,
        state: FSMContext,
):
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=message.from_user.id
    )
    post_topic = await PostTopicOffer.objects.acreate(
        text=message.text,
        telegram_user=telegram_user,
    )
    await message.answer(
        'Your message is accepted.\n'
        'Thank you for the feedback!',
        reply_markup=reply_english_menu_keyboard,
    )
    await send_post_topic_message_to_group(
        telegram_user=telegram_user,
        post_topic=post_topic
    )
    await state.clear()


@router.callback_query(F.data.startswith('contact_me_'))
async def contact_me_callback_handler(
        callback: types.CallbackQuery,
):
    if not callback.from_user.username:
        await callback.answer(
            'Перед отправкой запроса, '
            'добавьте пожалуйста username в свой телеграм аккаунт.\n'
            'Он нужен для обратной связи.\n\n'
            'Before sending the request, '
            'please add username to your telegram account.\n'
            "It's needed for feedback.",
            show_alert=True,
        )
        return
    telegram_user, _ = (
        await TelegramUser.objects
        .aget_or_create_by_from_user(from_user=callback.from_user)
    )
    post_id = callback.data.split('_')[-1]
    post_feedback_request_data = {
        'post_id': post_id,
        'telegram_user': telegram_user,
    }
    post_feedback_requests = await PostFeedBackRequest.objects.afilter(
        **post_feedback_request_data
    )
    await PostFeedBackRequest.objects.acreate(
        **post_feedback_request_data
    )
    if post_feedback_requests:
        await callback.answer(
            'Вы уже отправили запрос. '
            'Ожидайте ответа менеджера.\n\n',
            show_alert=True,
        )
        return

    await callback.answer(
        'Ваш запрос принят, '
        'скоро вам напишет ваш аккаунт-менеджер.',
        show_alert=True,
    )
    post_link = f'{settings.CHANNEL_LINK}/{callback.message.message_id}'

    manager_account = f'@{telegram_user.manager_account}' \
        if telegram_user.manager_account else 'нет'
    await callback.bot.send_message(
        text=(
            f'Пользователь @{telegram_user.username} '
            f'(ID: {telegram_user.telegram_id}) хочет '
            f'чтобы с ним связались по <a href="{post_link}">посту</a>\n\n'
            f'Менеджер: {manager_account}'
        ),
        chat_id=settings.CONTACT_GROUP_ID,
        parse_mode='HTML'
    )
