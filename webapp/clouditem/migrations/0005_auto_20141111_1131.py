# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clouditem', '0004_auto_20141111_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clouditem',
            name='itemTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
