# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('downloader', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField()),
                ('downTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('tokenID', models.ForeignKey(to='downloader.AccessToken')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
