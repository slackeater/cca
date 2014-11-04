# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20141104_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='DropboxAccountInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accountInfo', models.TextField(max_length=16777215)),
                ('metaTime', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('tokenID', models.ForeignKey(to='dashboard.DropboxToken')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DropboxFileMetadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('metadata', models.CharField(max_length=16384)),
                ('metaTime', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('tokenID', models.ForeignKey(to='dashboard.DropboxToken')),
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
