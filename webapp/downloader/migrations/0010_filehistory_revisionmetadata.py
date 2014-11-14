# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0009_auto_20141114_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='filehistory',
            name='revisionMetadata',
            field=models.TextField(default='-'),
            preserve_default=False,
        ),
    ]
