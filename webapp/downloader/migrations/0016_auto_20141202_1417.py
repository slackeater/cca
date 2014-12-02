# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0015_auto_20141130_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='threadStatus',
            field=models.IntegerField(default=b'-1'),
        ),
    ]
