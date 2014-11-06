# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20141105_1850'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleAccountInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accountInfo', models.TextField()),
                ('metaTime', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('tokenID', models.ForeignKey(to='dashboard.GoogleDriveToken')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
