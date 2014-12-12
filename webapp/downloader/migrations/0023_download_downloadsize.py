# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0022_download_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='downloadSize',
            field=models.TextField(default=0),
            preserve_default=True,
        ),
    ]
