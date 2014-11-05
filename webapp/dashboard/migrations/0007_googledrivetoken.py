# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0003_auto_20141028_1659'),
        ('dashboard', '0006_auto_20141104_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleDriveToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('encodedTokenInfo', models.TextField(max_length=65536)),
                ('userID', models.CharField(max_length=20)),
                ('importID', models.ForeignKey(to='importer.Upload')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
