from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from web.db.model_mixins import (
    AsyncBaseModel,
    TelegramMessageModelMixin
)

    
class Notification(AsyncBaseModel, TelegramMessageModelMixin):
    """Модель telegram уведомления"""

    receivers = models.ManyToManyField(
        'telegram_users.TelegramUser', 
        verbose_name=_('Получатели')
    )
    
    class Meta:
        verbose_name = _('Уведомление')
        verbose_name_plural = _('Уведомления')
    
    
class Post(AsyncBaseModel, TelegramMessageModelMixin):
    """Модель поста канала"""

    class Meta:
        verbose_name = _('Пост')
        verbose_name_plural = _('Посты')

    
class Poll(AsyncBaseModel):
    """Модель опроса"""
    question = models.CharField(
        _('Вопрос'),
        max_length=300,
    )
    created_at = models.DateTimeField(
        _('Время и дата создания'),
        auto_now_add=True
    )
    
    receivers = models.ManyToManyField(
        'telegram_users.TelegramUser', 
        verbose_name=_('Получатели')
    )
    
    class Meta:
        verbose_name = _('Опрос')
        verbose_name_plural = _('Опросы')

    def __str__(self):
        return self.question
    
    
class PollOption(AsyncBaseModel):
    """Модель варианта ответа опроса"""
    text = models.CharField(
        _('Ответ'),
        max_length=100,
    )
    
    poll = models.ForeignKey(
        'notifications.Poll',
        verbose_name=_('Опрос'),
        related_name='options',
        on_delete=models.CASCADE,
    )
    class Meta:
        verbose_name = _('Вариант ответа')
        verbose_name_plural = _('Варианты ответа')

    def __str__(self):
        return self.text