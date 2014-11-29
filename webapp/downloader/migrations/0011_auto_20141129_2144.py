# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0010_filehistory_revisionmetadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='verificationZIP',
            field=models.CharField(default=b'-', max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='download',
            name='verificationZIPHash',
            field=models.CharField(default=b'-', max_length=255),
            preserve_default=True,
        ),
    ]
