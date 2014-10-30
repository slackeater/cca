# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_dropboxfilemetadata'),
    ]

    operations = [
        migrations.CreateModel(
            name='DropboxAccountInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accountInfo', models.TextField(max_length=16777215)),
                ('metaTime', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('tokenID', models.ForeignKey(to='dashboard.DropboxToken')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
