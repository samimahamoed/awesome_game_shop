# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-23 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='image',
            field=models.ImageField(null=True, upload_to=b''),
        ),
    ]
