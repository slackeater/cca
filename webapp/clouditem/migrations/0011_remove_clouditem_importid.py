# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clouditem', '0010_remove_clouditem_reportername'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clouditem',
            name='importID',
        ),
    ]
