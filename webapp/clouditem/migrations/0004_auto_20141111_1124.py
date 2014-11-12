# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clouditem', '0003_clouditem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clouditem',
            name='itemTime',
            field=models.DateTimeField(),
        ),
    ]
