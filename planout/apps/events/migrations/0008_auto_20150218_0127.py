# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20150214_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='alternative_name',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='alternative_name',
        ),
        migrations.AddField(
            model_name='event',
            name='logo',
            field=core.fields.BaseImageField(storage=django.core.files.storage.FileSystemStorage(), max_length=1024, upload_to=core.fields.image_file_path, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='logo',
            field=core.fields.BaseImageField(storage=django.core.files.storage.FileSystemStorage(), max_length=1024, upload_to=core.fields.image_file_path, blank=True),
            preserve_default=True,
        ),
    ]
