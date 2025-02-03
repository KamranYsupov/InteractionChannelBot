from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.conf import settings

from .models import Notification, Post, Poll  
from web.services.telegram_service import telegram_service


@receiver(post_save, sender=Post)
def send_post_after_creation(sender, instance, created, **kwargs):
    if not created: 
        return 
    
    inline_keyboard = [
        [{
            'text': 'Свяжитесь со мной 📲',
            'callback_data': f'contact_me_{instance.id}'
        }],
        [{
            'text': 'Перейти в бота',
            'url': 'https://t.me/InteractionChannelBot?start=123'
        }]
    ]
            
    telegram_service.send_message(
        chat_id=settings.CHANNEL_ID,
        text=instance.text,
        reply_markup={'inline_keyboard': inline_keyboard}
    )
    
    
@receiver(post_save, sender=Poll)
def send_poll_after_creation(sender, instance, created, **kwargs):
    if not created:
        return

    def send_poll():
        receivers = instance.receivers.all()
        first_receiver = receivers[0]
        options_data = {}
        poll_options = []
        votes_data = {}
        
        for index, option in enumerate(instance.options.all()):
            poll_options.append(option.text)
            votes_data[index] = {option.id: []}
                        
        response = telegram_service.send_poll(
            chat_id=first_receiver.telegram_id,
            question=instance.question,
            options=poll_options
        )
        
        response_data = response.json()
        
        poll_id = response_data['result']['poll']['id']
        
        instance.poll_id = poll_id
        instance.votes_data = votes_data
        instance.save()
        
        for receiver in receivers[1:]:
            telegram_service.forward_message(
                chat_id=receiver.telegram_id,
                from_chat_id=first_receiver.telegram_id,
                message_id=response_data['result']['message_id']
            )
                        
    transaction.on_commit(send_poll)
    
    
@receiver(post_save, sender=Notification)
def send_notification_after_creation(sender, instance, created, **kwargs):
    if not created:
        return

    def send_notification():
        for receiver in instance.receivers.all():
            telegram_service.send_message(
                chat_id=receiver.telegram_id,
                text=instance.text
            )
            
    transaction.on_commit(send_notification)                                                              