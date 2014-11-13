# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clouditem', '0011_remove_clouditem_importid'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accessToken', models.TextField(max_length=65535)),
                ('userID', models.CharField(max_length=100)),
                ('serviceType', models.CharField(max_length=10)),
                ('tokenTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('userInfo', models.TextField()),
                ('cloudItem', models.ForeignKey(to='clouditem.CloudItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FileDownload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fileName', models.CharField(max_length=255)),
                ('alternateName', models.CharField(max_length=255)),
                ('status', models.IntegerField()),
                ('fileHistory', models.TextField()),
                ('downloadTime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FileHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('revision', models.CharField(max_length=255)),
                ('status', models.IntegerField()),
                ('fileDownloadID', models.ForeignKey(to='downloader.FileDownload')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FileMetadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('metadata', models.TextField()),
                ('metaTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('tokenID', models.ForeignKey(to='downloader.AccessToken')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='filedownload',
            name='metadataID',
            field=models.ForeignKey(to='downloader.FileMetadata'),
            preserve_default=True,
        ),
    ]
