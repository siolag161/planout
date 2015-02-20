# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djgeojson.fields
import core.fields
import events.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20150218_0127'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='occurrence',
            options={'ordering': ('start_time', 'end_time'), 'verbose_name': 'occurrence', 'verbose_name_plural': 'occurrences'},
        ),
        migrations.AlterField(
            model_name='event',
            name='age_range',
            field=events.fields.AgeRangeField(default=b'0-130', null=True, verbose_name='Age range', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=djgeojson.fields.PointField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=core.fields.AutoSlugField(db_index=True, max_length=250, null=True, verbose_name='Slug', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.URLField(null=True, verbose_name='website', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=core.fields.AutoSlugField(db_index=True, max_length=250, null=True, verbose_name='Slug', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='url',
            field=models.URLField(null=True, verbose_name='website', blank=True),
            preserve_default=True,
        ),
    ]
