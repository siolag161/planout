# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150227_1452'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='formatted_address',
            new_name='vicinity',
        ),
        migrations.RemoveField(
            model_name='location',
            name='gmap_url',
        ),
        migrations.RemoveField(
            model_name='location',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='location',
            name='website',
        ),
    ]
