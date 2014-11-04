# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_remove_mimetype_mimeid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dropboxaccountinfo',
            name='tokenID',
        ),
        migrations.DeleteModel(
            name='DropboxAccountInfo',
        ),
        migrations.RemoveField(
            model_name='dropboxfilemetadata',
            name='tokenID',
        ),
        migrations.DeleteModel(
            name='DropboxFileMetadata',
        ),
        migrations.DeleteModel(
            name='MimeType',
        ),
    ]
