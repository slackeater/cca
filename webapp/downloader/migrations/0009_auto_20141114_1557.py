# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0008_remove_filedownload_filehistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filedownload',
            name='metadataID',
        ),
        migrations.AddField(
            model_name='filedownload',
            name='tokenID',
            field=models.ForeignKey(default=2, to='downloader.AccessToken'),
            preserve_default=False,
        ),
    ]
