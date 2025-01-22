from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Poll, PollOption, Notification, Post



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
    fields = ('text', )
    extra = 2
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        if obj:
            return False
        return super().has_add_permission(request, obj)
    
    
@admin.register(Poll)
class PollAdmin(admin.ModelAdmin): 
    readonly_fields = ('created_at', )
    
    filter_horizontal = ('receivers', )
    
    inlines = [PollOptionInline]
    
    def has_change_permission(self, request, obj=None):
        return False 


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )
    
    filter_horizontal = ('receivers', )    
    
    def has_change_permission(self, request, obj=None):
        return False
    
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )
    
    def has_change_permission(self, request, obj=None):
        return False  
