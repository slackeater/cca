# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clouditem', '0005_auto_20141111_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='clouditem',
            name='desc',
            field=models.TextField(default='-'),
            preserve_default=False,
        ),
    ]
