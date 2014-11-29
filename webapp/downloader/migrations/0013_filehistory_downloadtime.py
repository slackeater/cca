# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0012_auto_20141129_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='filehistory',
            name='downloadTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
