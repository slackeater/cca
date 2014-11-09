# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20141108_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesstoken',
            name='tokentime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
