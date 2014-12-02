# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0016_auto_20141202_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='download',
            name='status',
        ),
    ]
