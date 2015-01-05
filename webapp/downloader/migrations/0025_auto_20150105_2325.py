# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0024_auto_20141212_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='endDownTime',
            field=models.DateTimeField(default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='download',
            name='finalFileSize',
            field=models.TextField(default=b'0'),
            preserve_default=True,
        ),
    ]
