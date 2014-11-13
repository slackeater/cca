# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clouditem', '0009_clouditem_reporterid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clouditem',
            name='reporterName',
        ),
    ]
