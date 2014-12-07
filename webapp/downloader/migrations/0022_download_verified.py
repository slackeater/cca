# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0021_auto_20141204_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='verified',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
