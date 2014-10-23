# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_login_pwd'),
    ]

    operations = [
        migrations.RenameField(
            model_name='login',
            old_name='pwd',
            new_name='password',
        ),
    ]
