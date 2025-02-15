from django.db import models
from django.utils.translation import gettext_lazy as _
from ulid import ULID

from .base_manager import AsyncBaseManager
        
        
def ulid_default() -> str:
    return str(ULID())
        
        
class AsyncBaseModel(models.Model):
    id = models.CharField( 
        primary_key=True,
        default=ulid_default,
        max_length=26,
        editable=False,
        unique=True,
        db_index=True,
    )
    
    objects = AsyncBaseManager()
    
    class Meta: 
        abstract = True
        
        
class AbstractTelegramUser(AsyncBaseModel):
    telegram_id = models.BigIntegerField(
        verbose_name=_('Телеграм ID'),
        unique=True,
        db_index=True,
    )
    username = models.CharField(
        _('Имя пользователя'),
        max_length=70,
        unique=True,
        db_index=True,
        null=True,
    )
    
    class Meta: 
        abstract = True
    
        
class TimestampMixin(models.Model):
    created_at = models.DateTimeField(
        _('Время и дата создания'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Время и дата последнего обновления'),
        auto_now=True
    )

    class Meta:
        abstract = True
        
        
class TelegramMessageModelMixin(models.Model):
    """Миксин для телеграм сообщения"""
    name = models.CharField(
        _('Название(опционально)'),
        max_length=150,
        null=True,
        blank=True,
        default=None,
    )
    text = models.TextField(
        _('Текст'),
        max_length=4000,
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
        abstract = True
        ordering = ['-created_at']
        
    def __str__(self):
        if self.name:
            return self.name
        
        return self.get_short_text()
    
    def get_short_text(self):
        if len(self.text) > 150:
            return f'{self.text[:150]}...'
        
        return self.text
    
    
class FeedBackMixin(models.Model):
    """Миксин обратной связи"""
    class Status:
        GOT = 'GOT'
        IN_PROGRESS = 'IN_PROGRESS'
        ANSWERED = 'ANSWERED'
        
        CHOICES = (
            (GOT, _('Получен')),
            (IN_PROGRESS, _('В работе')),
            (ANSWERED, _('Отвечен')),
        )
        
    text = models.TextField(
        _('Текст'),
        editable=False,
    )
    status = models.CharField(
        verbose_name=_('Статус'),
        max_length=15,
        choices=Status.CHOICES,
        default=Status.GOT,
        db_index=True,
    )
    created_at = models.DateTimeField(
        _('Время и дата создания'),
        auto_now_add=True
    )
    
    telegram_user = models.ForeignKey(
        'telegram_users.TelegramUser',
        verbose_name=_('Пользователь'), 
        on_delete=models.CASCADE,
        editable=False,
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']
        
    def __str__(self):
        return self.get_short_text()
    
    def get_short_text(self):
        if len(self.text) > 150:
            return f'{self.text[:150]}...'
        
        return self.text