# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountinfo',
            name='tokenID',
        ),
        migrations.DeleteModel(
            name='AccountInfo',
        ),
        migrations.RemoveField(
            model_name='filemetadata',
            name='tokenID',
        ),
        migrations.DeleteModel(
            name='FileMetadata',
        ),
        migrations.RemoveField(
            model_name='accesstoken',
            name='accessToken',
        ),
        migrations.RemoveField(
            model_name='accesstoken',
            name='importID',
        ),
        migrations.RemoveField(
            model_name='accesstoken',
            name='serviceType',
        ),
        migrations.RemoveField(
            model_name='accesstoken',
            name='tokentime',
        ),
        migrations.RemoveField(
            model_name='accesstoken',
            name='userID',
        ),
        migrations.AddField(
            model_name='accesstoken',
            name='a',
            field=models.TextField(default='a'),
            preserve_default=False,
        ),
    ]
