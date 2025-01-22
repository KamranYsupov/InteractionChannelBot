from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from web.db.model_mixins import (
    AsyncBaseModel,
    FeedBackRequestMixin
)


class PostFeedBackRequest(AsyncBaseModel, FeedBackRequestMixin):
    """Модель вопроса"""
    text = None # Исключаем поле FeedBackRequestMixin.text
    post = models.ForeignKey(
        "notifications.Post", 
        verbose_name=_("Пост"), 
        on_delete=models.CASCADE,
        db_index=True,
        editable=False,
    )
    
    class Meta:
        verbose_name = _('Заявка обратной связи по посту')
        verbose_name_plural = _('Заявки обратной связи по постам')
        
    
class FeedBackRequest(AsyncBaseModel, FeedBackRequestMixin):
    """Модель заявки обратной связи"""
    
    class Meta:
        verbose_name = _('Заявка обратной связи')
        verbose_name_plural = _('Заявки обратной связи')
        
        
class Question(AsyncBaseModel, FeedBackRequestMixin):
    """Модель вопроса"""
    
    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')
        
        
class PostTopicOffer(AsyncBaseModel, FeedBackRequestMixin):
    """Модель предложения темы поста"""
    
    class Meta:
        verbose_name = _('Предложение темы поста')
        verbose_name_plural = _('Предложения темы поста')

    