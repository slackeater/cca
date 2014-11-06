# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20141105_1850'),
        ('gdrivecloud', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleFileMetadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('metadata', models.TextField()),
                ('metaTime', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('tokenID', models.ForeignKey(to='dashboard.GoogleDriveToken')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
