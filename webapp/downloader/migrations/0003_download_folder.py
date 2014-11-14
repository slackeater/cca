# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0002_download'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='folder',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
    ]
