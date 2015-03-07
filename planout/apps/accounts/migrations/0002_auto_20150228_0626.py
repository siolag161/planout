# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import core.fields
import accounts.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicuser',
            name='avatar',
            field=accounts.fields.AvatarField(storage=django.core.files.storage.FileSystemStorage(), max_length=1024, upload_to=core.fields.image_file_path, blank=True),
            preserve_default=True,
        ),
    ]
