# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-11 23:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0006_auto_20170211_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.Profile'),
        ),
    ]
