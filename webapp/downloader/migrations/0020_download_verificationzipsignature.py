# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0019_auto_20141204_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='verificationZIPSignature',
            field=models.TextField(default=b'-'),
            preserve_default=True,
        ),
    ]
