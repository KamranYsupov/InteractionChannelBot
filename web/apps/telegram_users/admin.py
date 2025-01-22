from django.contrib import admin
from django.db.models import Q

from .models import TelegramUser, Company

    
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'telegram_id',
        'username', 
        'company', 
        'status',
        'manager_account',
        'time_joined',
    )   
    list_editable = ( 
        'company', 
        'status',
        'manager_account'
    )     
    list_filter = (
        'company', 
        'status', 
        'manager_account'
    )
    
    search_fields = (
        'telegram_id__iregex',
        'username__iregex',
    )
    readonly_fields = (
        'telegram_id',
        'username',
        'time_joined',
    )    


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name__iregex', )    

