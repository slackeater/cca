# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0020_download_verificationzipsignature'),
    ]

    operations = [
        migrations.RenameField(
            model_name='download',
            old_name='verificationZIPHash',
            new_name='verificationZIPSignatureHash',
        ),
    ]
