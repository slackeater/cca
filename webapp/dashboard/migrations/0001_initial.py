# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accessToken', models.TextField(max_length=65535)),
                ('userID', models.CharField(max_length=100)),
                ('serviceType', models.CharField(max_length=10)),
                ('tokentime', models.DateTimeField(default=django.utils.timezone.now)),
                ('importID', models.ForeignKey(to='importer.Upload')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AccountInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accountInfo', models.TextField()),
                ('metaTime', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('tokenID', models.ForeignKey(to='dashboard.AccessToken')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FileMetadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('metadata', models.TextField()),
                ('metaTime', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('tokenID', models.ForeignKey(to='dashboard.AccessToken')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MimeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mime', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
