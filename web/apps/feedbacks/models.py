from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from web.db.model_mixins import (
    AsyncBaseModel,
    FeedBackMixin
)


class PostFeedBackRequest(AsyncBaseModel, FeedBackMixin):
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
        
    def __str__(self):
        if self.post.name:
            post_text = self.post.name
        else:
            post_text = self.post.get_short_text()
            
        return f'@{self.telegram_user.username} - {post_text}'
    
        
    
class FeedBack(AsyncBaseModel, FeedBackMixin):
    """Модель обратной связи"""
    
    class Meta:
        verbose_name = _('Обратная связь')
        verbose_name_plural = _('Обратная связь')
        
        
class Question(AsyncBaseModel, FeedBackMixin):
    """Модель вопроса"""
    
    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')
        
        
class PostTopicOffer(AsyncBaseModel, FeedBackMixin):
    """Модель предложения темы поста"""
    status = None
    
    class Meta:
        verbose_name = _('Предложение темы поста')
        verbose_name_plural = _('Предложения темы поста')

    