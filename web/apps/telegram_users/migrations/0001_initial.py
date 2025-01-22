# Generated by Django 4.2.1 on 2025-01-22 17:27

from django.db import migrations, models
import django.db.models.deletion
import web.db.model_mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.CharField(db_index=True, default=web.db.model_mixins.ulid_default, editable=False, max_length=26, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.CharField(db_index=True, default=web.db.model_mixins.ulid_default, editable=False, max_length=26, primary_key=True, serialize=False, unique=True)),
                ('telegram_id', models.BigIntegerField(db_index=True, unique=True, verbose_name='Телеграм ID')),
                ('username', models.CharField(db_index=True, max_length=70, null=True, unique=True, verbose_name='Имя пользователя')),
                ('status', models.CharField(max_length=50, verbose_name='Должность')),
                ('manager_account', models.CharField(max_length=100, verbose_name='Аккаунт менеджера')),
                ('time_joined', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('company', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='telegram_users.company', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'Telegram пользователи',
                'ordering': ['-time_joined'],
            },
        ),
    ]
