import loguru
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from django.conf import settings

from web.apps.telegram_users.models import SuperGroupSettings, ChannelSettings
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
        'Мы здесь, чтобы помочь вам быстро решить вопрос. '
        'Опишите вашу ситуацию в следующем сообщении.',
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
        'Спасибо за доверие! Мы ценим ваше время, '
        'поэтому скоро с вами свяжется аккаунт-менеджер.',
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
        'Скажите, что нам улучшить или исправить? '
        'Обратная связь поступает напрямую в продуктовую команду.',
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
        'Спасибо, что поделились обратной связью. '
        'Каждое сообщение будет детально проработано '
        'и вы будете проинформированы о результате. ',
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
        'О чем вы бы хотели узнать? '
        'Какие темы вам интересны в наших постах? ',
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
        'Ваши идеи - наше вдохновение. '
        'Команда контента уже старается над созданием' 
        'полезного поста для вашего бизнеса.',
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
        'We are here to help you resolve your issue quickly. '
        'Please describe your situation in the next message. ',
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
        'Thank you for your trust! '
        'We value your time, so an account manager will contact you soon.',
        reply_markup=reply_english_menu_keyboard,
    )
    await send_question_message_to_group(
        telegram_user=telegram_user,
        question=question
    )
    await state.clear()


@router.message(
    F.text.casefold() == 'leave feedback 📤'
)
async def send_feedback_message_handler(
        message: types.Message,
        state: FSMContext,
):
    await message.answer(
        'What can we improve or amend? '
        'Your feedback goes directly to the product team. ',
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
        'Thank you for sharing your feedback. '
        'Every message will be carefully reviewed, '
        'and you will be informed of the outcome.',
        reply_markup=reply_english_menu_keyboard,
    )
    await send_feedback_message_to_group(
        telegram_user=telegram_user,
        feedback=feedback
    )
    await state.clear()


@router.message(
    F.text.casefold() == 'suggest a post topic 📝'
)
async def offer_post_topic_message_handler(
        message: types.Message,
        state: FSMContext,
):
    await message.answer(
        'What would you like to learn about? '
        'What topics interest you in our posts? ',
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
    group_settings: SuperGroupSettings = await sync_to_async(SuperGroupSettings.load)()
    channel_settings: ChannelSettings = await sync_to_async(ChannelSettings.load)()

    post_link = f'{channel_settings.channel_link}/{callback.message.message_id}'

    manager_account = f'@{telegram_user.manager_account}' \
        if telegram_user.manager_account else 'нет'
    await callback.bot.send_message(
        text=(
            f'Пользователь @{telegram_user.username} '
            f'(ID: {telegram_user.telegram_id}) хочет, '
            f'чтобы с ним связались по <a href="{post_link}">посту</a>\n\n'
            f'Менеджер: {manager_account}'
        ),
        chat_id=group_settings.group_id,
        parse_mode='HTML'
    )
