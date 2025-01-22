from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from web.db.model_mixins import (
    AsyncBaseModel,
    AbstractTelegramUser,
)


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


    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('Telegram пользователи')
        ordering = ['-time_joined']

    def __str__(self):
        return self.username
    
    
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


