# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0007_auto_20141114_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filedownload',
            name='fileHistory',
        ),
    ]
