from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from web.db.model_mixins import (
    AsyncBaseModel,
)

    
class Notification(AsyncBaseModel):
    """Модель telegram уведомления"""
    name = models.CharField(
        _("Название(опционально)"),
        max_length=150,
        null=True,
        blank=True,
        default=None,
    )
    text = models.TextField(_("Текст"))
    is_send = models.BooleanField(
        _("Отправить?"),
        default=False,
    )
    
    class Meta:
        verbose_name = _("Уведомление")
        verbose_name_plural = _("Уведомления")

    def __str__(self):
        if self.name:
            return self.name
        if len(self.text) > 100:
            return f'{self.text[:100]}...'
        
        return self.text
    
    
class Poll(AsyncBaseModel):
    """Модель опроса"""
    question = models.CharField(
        _("Вопрос"),
        max_length=300,
    )
    is_send = models.BooleanField(
        _("Отправить?"),
        default=False,
    )
    
    class Meta:
        verbose_name = _("Опрос")
        verbose_name_plural = _("Опросы")

    def __str__(self):
        return self.question
    
    
class PollOption(AsyncBaseModel):
    """Модель опросника"""
    text = models.CharField(
        _("Ответ"),
        max_length=100,
    )
    votes_count = models.PositiveBigIntegerField(
        _("Количество голосов"),
        default=0
    )
    
    poll = models.ForeignKey(
        "notifications.Poll",
        verbose_name=_("Опрос"),
        related_name='options',
        on_delete=models.CASCADE,
    )
    class Meta:
        verbose_name = _("Вариант ответа")
        verbose_name_plural = _("Варианты ответа")

    def __str__(self):
        return self.text