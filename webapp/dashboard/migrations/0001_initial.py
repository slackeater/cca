# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0003_auto_20141028_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='DropboxToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accessToken', models.CharField(max_length=256)),
                ('userID', models.CharField(max_length=20)),
                ('importID', models.ForeignKey(to='importer.Upload')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
