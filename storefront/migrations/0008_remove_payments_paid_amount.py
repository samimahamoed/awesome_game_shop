# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-11 23:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0007_auto_20170211_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payments',
            name='paid_amount',
        ),
    ]
