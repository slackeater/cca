# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reporterName', models.CharField(max_length=20)),
                ('itemTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('importID', models.ForeignKey(to='importer.Upload')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
