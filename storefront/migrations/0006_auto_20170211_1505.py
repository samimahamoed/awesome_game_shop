# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-11 23:05
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import storefront.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storefront', '0005_auto_20170131_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Developers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('starting_date', models.DateTimeField(default=datetime.datetime.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.IntegerField(unique=True)),
                ('paid_amount', models.FloatField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='game',
            name='players',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='nickname',
        ),
        migrations.AddField(
            model_name='profile',
            name='games',
            field=models.ManyToManyField(to='storefront.Game'),
        ),
        migrations.AddField(
            model_name='profile',
            name='height',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_img_path',
            field=models.ImageField(default='profile/placeholder.png', height_field='height', storage=storefront.models.OverwriteStorage(), upload_to=storefront.models.profile_img_location, width_field='width'),
        ),
        migrations.AddField(
            model_name='profile',
            name='width',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='game',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(blank=True, default='image_uploads/placeholder.png', null=True, upload_to='image_uploads'),
        ),
        migrations.AlterField(
            model_name='game',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='payments',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='storefront.Profile'),
        ),
        migrations.AddField(
            model_name='payments',
            name='developer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.Developers'),
        ),
        migrations.AddField(
            model_name='payments',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.Game'),
        ),
        migrations.AddField(
            model_name='game',
            name='developer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='storefront.Developers'),
            preserve_default=False,
        ),
    ]