# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-30 02:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storefront', '0003_auto_20170127_0030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=512)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(null=True, upload_to='image_uploads')),
            ],
        ),
        migrations.CreateModel(
            name='Gamesettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField()),
                ('width', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Gamestate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_information', models.CharField(blank=True, max_length=512)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Highscore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_nickname', models.CharField(max_length=15)),
                ('score', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='game',
            name='created',
        ),
        migrations.AddField(
            model_name='game',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='description',
            field=models.TextField(default=0),
        ),
        migrations.AddField(
            model_name='highscore',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.Game'),
        ),
        migrations.AddField(
            model_name='highscore',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.Profile'),
        ),
        migrations.AddField(
            model_name='gamestate',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.Game'),
        ),
        migrations.AddField(
            model_name='gamestate',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.Profile'),
        ),
        migrations.AddField(
            model_name='gamesettings',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.Game'),
        ),
        migrations.AddField(
            model_name='gamesettings',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.Profile'),
        ),
        migrations.AddField(
            model_name='achievement',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.Game'),
        ),
        migrations.AddField(
            model_name='achievement',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storefront.Profile'),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(to='storefront.Profile'),
        ),
    ]
