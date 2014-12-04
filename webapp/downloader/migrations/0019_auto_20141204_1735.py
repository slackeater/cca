# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0018_auto_20141204_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='verificationZIPHash',
            field=models.TextField(default=b'-'),
        ),
    ]
