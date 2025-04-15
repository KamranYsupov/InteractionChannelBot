from django.db import transaction
import pandas as pd

from web.apps.telegram_users.models import TelegramUser, Company


def clean_value(val):
    return None if pd.isna(val) else val


def import_devices_from_excel(excel_file):
    """Функция для импрота в данных из excel таблицы в бд"""
    df = pd.read_excel(excel_file)

    with transaction.atomic():
        for index, row in df.iterrows():
            company_name = clean_value(row.get('Компания'))
            company, _ = Company.objects.get_or_create(
                name=company_name
            ) if company_name else (None, False)

            status = clean_value(row.get('Должность'))
            status = status.upper() if status else None

            manager_account = clean_value(row.get('Аккаунт менеджер'))
            username = clean_value(row.get('Контакт'))

            if username and username.startswith('https://t.me/'):
                username = username.split('/')[-1]


            TelegramUser.objects.update_or_create(
                username=username,
                defaults={
                    'company': company,
                    'status': status,
                    'manager_account': manager_account
                }
            )
