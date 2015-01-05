# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0026_auto_20150105_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='endDownTime',
            field=models.DateTimeField(blank=True),
        ),
    ]
