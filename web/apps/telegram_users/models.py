from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from asgiref.sync import sync_to_async

from web.db.model_mixins import (
    AsyncBaseModel,
    AbstractTelegramUser,
)
from web.db.base_manager import AsyncBaseManager
from aiogram.types import User


class TelegramUserManager(AsyncBaseManager):
    async def aget_or_create_by_from_user(
        self,
        from_user: User,
    ):
        obj, created = await super().aget_or_create(
            telegram_id=from_user.id,
            defaults={'username': from_user.username}
        )
        
        if not created and obj.username != from_user.username:
            obj.username = from_user.username
            await obj.asave()
        
        return obj, created


class TelegramUser(AbstractTelegramUser):
    """Модель telegram пользователя"""
    
    class Status:
        TOP = 'TOP'
        MANAGER = 'MANAGER'
        SENIOR = 'SENIOR'
        
        choices = (
            (TOP, _('TOP')),
            (MANAGER, _('Manager')),
            (SENIOR, _('Senior')),
        )
        
    
    status = models.CharField(
        _('Должность'),
        max_length=50,
        choices=Status.choices,
        null=True,
        default=None,
        blank=True,
    )
    manager_account = models.CharField(
        _('Аккаунт менеджера'),
        max_length=100,
        null=True,
        default=None,
        blank=True,
    )
    comment = models.CharField(
        _('Комментарий'),
        max_length=150,
        blank=True,
    )
    time_joined = models.DateTimeField(
        _('Время добавления'),
        auto_now_add=True
    )
    
    company = models.ForeignKey(
        'telegram_users.Company', 
        verbose_name=_('Компания'), 
        on_delete=models.CASCADE,
        null=True,
        default=None,
        blank=True,
    )
    
    objects = TelegramUserManager()
    
    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('Telegram пользователи')
        ordering = ['-time_joined']

    def __str__(self):
        return self.username if self.username \
            else f'Пользователь {self.telegram_id}'
    
    
class Company(AsyncBaseModel):
    """Модель компании"""
    name = models.CharField(
        _('Название'),
        max_length=150,
        unique=True,
    )
    
    class Meta:
        verbose_name = _('Компания')
        verbose_name_plural = _('Компании')

    def __str__(self):
        return self.name


