# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0011_auto_20141129_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='filedownload',
            name='fileHash',
            field=models.CharField(default=b'-', max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='filehistory',
            name='fileRevisionHash',
            field=models.CharField(default=b'-', max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='filehistory',
            name='revisionMetadataHash',
            field=models.CharField(default=b'-', max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='filemetadata',
            name='metadataHash',
            field=models.CharField(default=b'-', max_length=255),
            preserve_default=True,
        ),
    ]
