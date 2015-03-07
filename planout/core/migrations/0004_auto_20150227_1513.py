# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150227_1503'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='placeId',
            new_name='place_id',
        ),
    ]
