# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_location_coordinates'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='coordinates',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='longitude/latitude', blank=True),
            preserve_default=True,
        ),
    ]
