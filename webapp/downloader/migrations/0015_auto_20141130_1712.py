# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0013_filehistory_downloadtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedownload',
            name='fileHash',
            field=models.TextField(default=b'-'),
        ),
        migrations.AlterField(
            model_name='filehistory',
            name='fileRevisionHash',
            field=models.TextField(default=b'-'),
        ),
        migrations.AlterField(
            model_name='filehistory',
            name='revisionMetadataHash',
            field=models.TextField(default=b'-'),
        ),
        migrations.AlterField(
            model_name='filemetadata',
            name='metadataHash',
            field=models.TextField(default=b'-'),
        ),
    ]
