import loguru
from aiogram import Router, types, F
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated
from aiogram.enums import ChatMemberStatus
from django.conf import settings
from asgiref.sync import sync_to_async

from models import TelegramUser, Poll, PollOption
from loader import bot
from web.services.telegram_service import telegram_service


router = Router()


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def user_subs_channel_handler(event: ChatMemberUpdated):
    if event.new_chat_member.status == ChatMemberStatus.MEMBER:
        telegram_user, created = (
            await TelegramUser.objects
            .aget_or_create_by_from_user(from_user=event.from_user)
        )
        
        
@router.poll_answer()
async def poll_answer_handler(poll_answer: types.PollAnswer):
    poll = await Poll.objects.aget(poll_id=int(poll_answer.poll_id))
    telegram_user = await TelegramUser.objects.aget(
        telegram_id=poll_answer.user.id
    )
    
    if None in (poll, telegram_user):
        return
    
    if poll_answer.option_ids != []:
        for option_index in poll_answer.option_ids:
            print(poll.votes_data)
            option_data = poll.votes_data[str(option_index)]
            option_id = list(option_data.keys())[0]
            poll.votes_data[str(option_index)][option_id].append(poll_answer.user.id)
            
            poll_option = await PollOption.objects.aget(id=option_id)
            await sync_to_async(poll_option.voters.add)(telegram_user)
            await poll_option.asave()
        
        await poll.asave()
        return
           
    for option_index, option_data in poll.votes_data.items():
        option_id = list(option_data.keys())[0]
        votes = poll.votes_data[str(option_index)][option_id]
        if poll_answer.user.id not in votes:
            continue
        
        poll.votes_data[str(option_index)][option_id].remove(poll_answer.user.id)
        
        poll_option = await PollOption.objects.aget(id=option_id)
        await sync_to_async(poll_option.voters.remove)(telegram_user)
        await poll_option.asave()
        
    await poll.asave()
    
        
        
    