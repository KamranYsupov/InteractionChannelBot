from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from web.db.model_mixins import (
    AsyncBaseModel,
)

    
class Event(AsyncBaseModel):
    """Модель мероприятия"""
    name = models.CharField(
        _('Название'),
        max_length=150,
    )
    date = models.DateField(
        _('Дата проведения'),
        auto_now=False,
        auto_now_add=False
    )
    register_link = models.URLField(
        _('Ссылка на регистрацию'), 
        max_length=200
    )
    
    members = models.ManyToManyField(
        'telegram_users.TelegramUser', 
        verbose_name=_('Участники')
    )
    
    class Meta:
        verbose_name = _('Мероприятие')
        verbose_name_plural = _('Мероприятия')
        ordering = ['-date']

    def __str__(self):
        return self.name

