# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
        ('cloudservice', '0002_auto_20141110_2235'),
    ]

    operations = [
        migrations.CreateModel(
            name='Downloads',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dirName', models.CharField(max_length=255)),
                ('downTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.IntegerField(max_length=1)),
                ('tokenID', models.ForeignKey(to='dashboard.AccessToken')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
