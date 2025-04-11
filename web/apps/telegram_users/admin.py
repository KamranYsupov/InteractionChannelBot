from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import TelegramUser, Company, ChannelSettings, SuperGroupSettings
from ...admin.mixins import SingletonModelAdminMixin


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
    list_filter = (
        'company', 
        'status', 
        'manager_account'
    )
    list_editable = (
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

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return self.readonly_fields

        return []


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name__iregex', )


@admin.register(ChannelSettings)
class ChannelSettingsAdmin(SingletonModelAdminMixin):
    pass


@admin.register(SuperGroupSettings)
class SuperGroupSettingsAdmin(SingletonModelAdminMixin):
    pass
