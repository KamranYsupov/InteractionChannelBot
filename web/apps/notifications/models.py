from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from web.db.model_mixins import (
    AsyncBaseModel,
    TelegramMessageModelMixin,
    TimestampMixin
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
    poll_id = models.PositiveBigIntegerField(
        _('Telegram Poll ID'),
        unique=True,
        db_index=True,
        null=True,
        blank=True,
        default=None
    )
    question = models.CharField(
        _('Вопрос'),
        max_length=300,
    )
    votes_data = models.JSONField(
        _('Данные голосов'),
        default=dict
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
    
    
class PollOption(AsyncBaseModel, TimestampMixin):
    """Модель варианта ответа опроса"""
    text = models.CharField(
        _('Ответ'),
        max_length=100,
    )
    updated_at = None
    
    voters = models.ManyToManyField(
        'telegram_users.TelegramUser', 
        verbose_name=_('Пользоветели')
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
        ordering = ['created_at']

    def __str__(self):
        return self.text