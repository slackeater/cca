# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='parsed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='upload',
            name='uploadDate',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='upload',
            name='uploadIP',
            field=models.IPAddressField(default=b'0.0.0.0', blank=True),
            preserve_default=True,
        ),
    ]
