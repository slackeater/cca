# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0004_auto_20141114_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='threadStatus',
            field=models.CharField(default=None, max_length=10),
            preserve_default=True,
        ),
    ]
