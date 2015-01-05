# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0025_auto_20150105_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='endDownTime',
            field=models.DateTimeField(default=None, blank=True),
        ),
    ]
