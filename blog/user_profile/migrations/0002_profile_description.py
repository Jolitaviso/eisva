# Generated by Django 5.0.2 on 2024-03-11 20:06

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='description',
            field=tinymce.models.HTMLField(blank=True, max_length=10000, null=True, verbose_name='description'),
        ),
    ]
