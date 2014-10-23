# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_remove_login_pwd'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='pwd',
            field=models.CharField(default=None, max_length=256),
            preserve_default=False,
        ),
    ]
