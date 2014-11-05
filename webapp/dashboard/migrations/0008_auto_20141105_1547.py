# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_googledrivetoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googledrivetoken',
            name='encodedTokenInfo',
            field=models.TextField(max_length=65535),
        ),
    ]
