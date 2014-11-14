# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0003_download_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='folder',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
