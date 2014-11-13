# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clouditem', '0011_remove_clouditem_importid'),
        ('importer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='cloudItemID',
            field=models.ForeignKey(default=29, to='clouditem.CloudItem'),
            preserve_default=False,
        ),
    ]
