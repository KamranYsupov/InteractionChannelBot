# Generated by Django 4.2.1 on 2025-01-22 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_users', '0001_initial'),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='polloption',
            name='votes_count',
        ),
        migrations.AddField(
            model_name='polloption',
            name='voters',
            field=models.ManyToManyField(to='telegram_users.telegramuser', verbose_name='Пользоветели'),
        ),
    ]
