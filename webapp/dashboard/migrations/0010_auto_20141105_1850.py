# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20141105_1812'),
    ]

    operations = [
        migrations.RenameField(
            model_name='googledrivetoken',
            old_name='encodedTokenInfo',
            new_name='accessToken',
        ),
    ]
