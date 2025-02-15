from django.contrib import admin, messages
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Poll, PollOption, Notification, Post
from web.apps.feedbacks.models import PostFeedBackRequest


class PollOptionFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        
        valid_options = [
            cleaned_data for cleaned_data in self.cleaned_data
            if cleaned_data and not cleaned_data.get('DELETE', False)
        ]
        
        if len(valid_options) < 2:
            raise ValidationError("Опрос должен содержать как минимум 2 варианта ответа.")
        if len(valid_options) > 10:
            raise ValidationError("Опрос не может содержать более 10 вариантов ответа.")
        
        
class PollOptionInline(admin.TabularInline):
    model = PollOption
    formset = PollOptionFormSet
    fields = ('text', 'votes_count', 'voters')
    readonly_fields = ('votes_count', 'voters')
    extra = 2
    
    def votes_count(self, obj) -> int:
        return obj.voters.count()
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        if obj:
            return False
        return super().has_add_permission(request, obj)
    
    votes_count.short_description = 'Количество голосов'


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    exclude = ('poll_id', 'votes_data', 'is_published',)
    readonly_fields = ('created_at', )
    search_fields = ('question__iregex', )

    filter_horizontal = ('receivers', )
    
    inlines = [PollOptionInline]
    
    def has_change_permission(self, request, obj=None):
        return False 


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    search_fields = (
        'name__iregex', 
        'text__iregex',
    )
    readonly_fields = ('created_at', )

    filter_horizontal = ('receivers', )

    def has_change_permission(self, request, obj=None):
        return False
    
  
class PostFeedBackRequestInline(admin.TabularInline):
    model = PostFeedBackRequest
    fields = (
        'telegram_user',
        'status',
        'created_at'
    )
    readonly_fields = (
        'telegram_user',
        'created_at',
    )
    
    def has_add_permission(self, request, obj=None):
        return False
    
      
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = (
        'name__iregex', 
        'text__iregex',
    )
    readonly_fields = ('text', 'created_at', )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.inlines = (PostFeedBackRequestInline, )
            return self.readonly_fields
        
        return []
        
    
 
