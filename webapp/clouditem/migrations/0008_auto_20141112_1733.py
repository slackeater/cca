# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clouditem', '0007_clouditem_reportname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clouditem',
            name='importID',
            field=models.ForeignKey(to='importer.Upload', null=True),
        ),
    ]
