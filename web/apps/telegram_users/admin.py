from django.contrib import admin

from .models import TelegramUser, Company


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'telegram_id',
        'username', 
        'company', 
        'status',
        'manager_account'
    )   
    list_editable = ( 
        'company', 
        'status',
        'manager_account'
    )     
    
    #readonly_fields = ('telegram_id', )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass    

