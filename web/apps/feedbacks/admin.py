from django.contrib import admin

from .models import (
    PostFeedBackRequest,
    FeedBack,
    Question,
    PostTopicOffer
)


class FeedBackAdminMixin:
    list_display = ('short_text', 'status')
    list_editable = ('status', )
    list_filter = ('status', )
    
    fields = ('text', 'status', 'telegram_user', 'created_at')
    readonly_fields = ('text', 'telegram_user', 'created_at')

    @admin.display(description='Текст')
    def short_text(self, obj):
        return obj.get_short_text()
    
    
@admin.register(PostFeedBackRequest)
class PostFeedBackRequestAdmin(admin.ModelAdmin): 
    list_display = (
        'telegram_user',
        'status',
        'post', 
        'created_at'
    )
    list_editable = ('status', )
    list_filter = ('post', ) 
    
    fields = (
        'telegram_user',
        'status',
        'post', 
        'created_at'
    )
    readonly_fields = (
        'post',
        'telegram_user',
        'created_at',
    )
    
    
@admin.register(FeedBack)
class FeedBackAdmin(FeedBackAdminMixin, admin.ModelAdmin):
    pass 
    
    
@admin.register(Question)
class QuestionAdmin(FeedBackAdminMixin, admin.ModelAdmin): 
    search_fields = ('text__iregex', )
    
    
@admin.register(PostTopicOffer)
class PostTopicOfferAdmin(admin.ModelAdmin): 
    list_display = ('short_text', )
    
    fields = ('topic', 'telegram_user', 'created_at', )
    readonly_fields = ('topic', 'telegram_user', 'created_at', )
    
    @admin.display(description='Тема')
    def short_text(self, obj):
        return obj.get_short_text()
    
    @admin.display(description='Тема')
    def topic(self, obj):
        return obj.text
    