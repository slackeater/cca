# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Downloads',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dirName', models.CharField(max_length=255)),
                ('downTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.IntegerField(max_length=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
