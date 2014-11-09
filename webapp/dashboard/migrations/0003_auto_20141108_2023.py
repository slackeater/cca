# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20141108_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesstoken',
            name='accessToken',
            field=models.TextField(max_length=65535),
        ),
    ]
