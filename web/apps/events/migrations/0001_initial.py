# Generated by Django 4.2.1 on 2025-01-22 16:53

from django.db import migrations, models
import web.db.model_mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('telegram_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.CharField(db_index=True, default=web.db.model_mixins.ulid_default, editable=False, max_length=26, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('location', models.CharField(max_length=150, verbose_name='Локация')),
                ('date', models.DateField(verbose_name='Дата проведения')),
                ('register_link', models.URLField(verbose_name='Ссылка на регистрацию')),
                ('members', models.ManyToManyField(to='telegram_users.telegramuser', verbose_name='Участники')),
            ],
            options={
                'verbose_name': 'Мероприятие',
                'verbose_name_plural': 'Мероприятия',
                'ordering': ['-date'],
            },
        ),
    ]
