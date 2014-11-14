# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0005_download_threadstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='threadMessafe',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='download',
            name='threadStatus',
            field=models.CharField(default=b'stopped', max_length=10),
        ),
    ]
