import loguru
from aiogram import Router, types, F
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from django.conf import settings
from asgiref.sync import sync_to_async

from models import (
    TelegramUser,
    Event
) 
from keyboards.inline import get_inline_keyboard
from utils.pagination import Paginator, get_pagination_buttons
from utils.message import get_event_message_info
from utils.bot import edit_text_or_answer, send_take_part_event_message_to_group

router = Router()

async def events_message_handler(
    telegram_obj: types.Message | types.CallbackQuery,
    in_english: bool = False,
):
    if in_english:
        language_code = 'en'
        text = 'Choice an event.'
    else:
        language_code = 'ru'   
        text = 'Выберите мероприятие.'     
    
    if isinstance(telegram_obj, types.Message):
        page_number = 1
        message = telegram_obj
    else:
        page_number = int(telegram_obj.data.split('_')[-1])
        message = telegram_obj.message
        
    events = await Event.objects.a_all()
    
    paginator = Paginator(
        array=events,
        per_page=5,
        page_number=page_number
    )
    
    buttons = {
        event.name: f'{language_code}_event_{event.id}_{page_number}' 
        for event in paginator.get_page()
    }
    pagination_buttons = get_pagination_buttons(
        paginator, 
        prefix=f'{language_code}_events',
        in_english=in_english,
    )
    
    sizes = (1, ) * len(buttons) 
    sizes += (2, 1) if len(pagination_buttons) == 2 else (1, 1)
    
    buttons.update(pagination_buttons)
    await edit_text_or_answer(
        message,
        text=text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=sizes,
        )
    )
    

@router.message(
    F.text.casefold() == 'посмотреть календарь мероприятий 📅'
)
@router.callback_query(F.data.startswith('ru_events_'))
async def ru_events_message_handler(
    telegram_obj: types.Message | types.CallbackQuery,
    state: FSMContext,
):
    await events_message_handler(telegram_obj, in_english=False)
    
      
@router.message(
    F.text.casefold() == 'events calendar 📅'
)
@router.callback_query(F.data.startswith('en_events_'))
async def en_events_message_handler(
    telegram_obj: types.Message | types.CallbackQuery,
    state: FSMContext,
):
    await events_message_handler(telegram_obj, in_english=True)


async def event_callback_handler(
    callback: types.CallbackQuery,
    in_english: bool = False,
):
    if in_english:
        buttons_labels = ("I'll take part", 'Back 🔙' )
        language_code = 'en'
    else:
        buttons_labels = ('Буду участвовать', 'Назад 🔙')
        language_code = 'ru'
        
    event_id, page_number = callback.data.split('_')[2:]
    buttons = {}

    telegram_user = await TelegramUser.objects.aget(
        telegram_id=callback.from_user.id
    )
    event = await Event.objects.aget(id=event_id)
    
    if telegram_user not in await sync_to_async(list)(event.members.all()):
        buttons[buttons_labels[0]] = f'{language_code}_part_{event_id}_{page_number}'
        
    buttons[buttons_labels[1]] = f'{language_code}_events_{page_number}'
        
    message_text = get_event_message_info(event, in_english=in_english)
        
    await callback.message.edit_text(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=(1, 1)
        ),
        parse_mode='HTML'
    )
    

@router.callback_query(F.data.startswith('en_event_'))
async def en_event_callback_handler(
    callback: types.CallbackQuery,
):
    await event_callback_handler(callback, in_english=True)


@router.callback_query(F.data.startswith('ru_event_'))
async def ru_event_callback_handler(
    callback: types.CallbackQuery,
):
    await event_callback_handler(callback, in_english=False)
    
    
async def take_part_callback_handler(
    callback: types.CallbackQuery,
    in_english: bool = False,
):
    if in_english:
        message_text = "You have been added to the participants's list ✅"
        back_button_label = 'Back 🔙'
        language_code = 'en'
    else:
        message_text = 'Вы добавлены в список участников ✅'
        back_button_label = 'Назад 🔙'
        language_code = 'ru'
        
    event_id, page_number = callback.data.split('_')[2:]

    buttons = {back_button_label: f'{language_code}_events_{page_number}'}
    
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=callback.from_user.id
    )
    event = await Event.objects.aget(id=event_id)
    await sync_to_async(event.members.add)(telegram_user)
    
    await send_take_part_event_message_to_group(
        telegram_user=telegram_user,
        event=event
    )
    await callback.message.edit_text(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=(1, 1)
        ),
        parse_mode='HTML'
    )
    
    
@router.callback_query(F.data.startswith('ru_part_'))
async def ru_take_part_callback_handler(
    callback: types.CallbackQuery,
):
    await take_part_callback_handler(
        callback,
        in_english=False
    )
    
    
@router.callback_query(F.data.startswith('en_part_'))
async def en_take_part_callback_handler(
    callback: types.CallbackQuery,
):
    await take_part_callback_handler(
        callback,
        in_english=True
    )
