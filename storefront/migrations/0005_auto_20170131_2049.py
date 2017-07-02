# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-31 20:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0004_auto_20170129_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='description',
            field=models.TextField(blank=True, default=b''),
        ),
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=b'image_uploads'),
        ),
    ]
