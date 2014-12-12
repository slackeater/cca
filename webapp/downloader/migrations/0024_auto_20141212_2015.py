# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0023_download_downloadsize'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='downloadSize',
            field=models.BigIntegerField(default=0),
        ),
    ]
