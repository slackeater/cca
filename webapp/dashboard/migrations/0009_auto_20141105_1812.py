# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20141105_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googledrivetoken',
            name='encodedTokenInfo',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='googledrivetoken',
            name='userID',
            field=models.CharField(max_length=50),
        ),
    ]
