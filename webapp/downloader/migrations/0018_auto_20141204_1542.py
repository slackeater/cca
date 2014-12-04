# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0017_remove_download_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='verificationZIP',
            field=models.BooleanField(default=False),
        ),
    ]
