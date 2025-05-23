# Generated by Django 4.2.1 on 2025-02-03 15:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_remove_polloption_votes_count_polloption_voters'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='polloption',
            options={'ordering': ['created_at'], 'verbose_name': 'Вариант ответа', 'verbose_name_plural': 'Варианты ответа'},
        ),
        migrations.AddField(
            model_name='polloption',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Время и дата создания'),
            preserve_default=False,
        ),
    ]
