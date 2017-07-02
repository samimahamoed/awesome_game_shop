# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-12 00:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0010_auto_20170211_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='paid_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='payments',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]