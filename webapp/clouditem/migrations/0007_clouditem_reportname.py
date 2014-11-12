# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clouditem', '0006_clouditem_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='clouditem',
            name='reportName',
            field=models.CharField(default='-', max_length=20),
            preserve_default=False,
        ),
    ]
