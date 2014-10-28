# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0002_auto_20141024_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='uploadDate',
            field=models.DateTimeField(default=django.utils.timezone.now, blank=True),
        ),
    ]
