# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dropcloud', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dropboxfilemetadata',
            name='metadata',
            field=models.CharField(max_length=16777125),
        ),
    ]
