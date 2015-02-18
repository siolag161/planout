# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150212_0612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basicuser',
            name='username_uuid',
        ),
        migrations.AddField(
            model_name='basicuser',
            name='uuid',
            field=django_extensions.db.fields.ShortUUIDField(default='', editable=False, blank=True),
            preserve_default=False,
        ),
    ]
