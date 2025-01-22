from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date', 
        'register_link'
    )   
    
    search_fields = (
        'name__iregex',
    )
    readonly_fields = ('members', )  
