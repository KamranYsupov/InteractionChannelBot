from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Poll, PollOption, Notification



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
    
    
@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question',)
    
    inlines = [PollOptionInline]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass    
