import loguru
from aiogram import Router, types, F
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from django.conf import settings

from models import (
    TelegramUser,
    Event
) 
from keyboards.inline import get_inline_keyboard
from utils.pagination import Paginator, get_pagination_buttons
from utils.message import get_event_message_info
from utils.bot import edit_text_or_answer

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
    

@router.callback_query(
    or_f(
        F.data.startswith('ru_event_'),
        F.data.startswith('en_event_')
    )
)
async def change_language_handler(
    callback: types.CallbackQuery,
):
    
    language_code, _, event_id, page_number = callback.data.split('_')
    if language_code == 'en':
        in_english = True 
        buttons_labels = ("I'll take part", 'Back 🔙') 
    else:
        in_english = False
        buttons_labels = ('Буду участвовать', 'Назад 🔙') 
        
    buttons_values = (
        f'{language_code}_part_{event_id}_{page_number}',
        f'{language_code}_events_{page_number}'
    )
    buttons = dict(zip(buttons_labels, buttons_values))
    
    event = await Event.objects.aget(id=event_id)
    message_text = get_event_message_info(event, in_english=in_english)
        
    await callback.message.edit_text(
        message_text,
        reply_markup=get_inline_keyboard(
            buttons=buttons,
            sizes=(1, 1)
        ),
        parse_mode='HTML'
    )
    
    
    