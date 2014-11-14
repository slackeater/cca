# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0006_auto_20141114_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='download',
            name='threadMessafe',
        ),
        migrations.AddField(
            model_name='download',
            name='threadMessage',
            field=models.TextField(default=b'-'),
            preserve_default=True,
        ),
    ]
