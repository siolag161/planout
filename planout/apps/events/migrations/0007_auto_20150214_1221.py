# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.fields
import events.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20150212_0845'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='end_end',
            new_name='end_time',
        ),
        migrations.RenameField(
            model_name='occurrence',
            old_name='end_end',
            new_name='end_time',
        ),
        migrations.AddField(
            model_name='event',
            name='is_online',
            field=models.BooleanField(default=False, verbose_name="It's an online event"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='age_range',
            field=events.fields.AgeRangeField(default=b'0-130', verbose_name='Age range'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=core.fields.AutoSlugField(max_length=250, null=True, verbose_name='Slug', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=core.fields.AutoSlugField(max_length=250, null=True, verbose_name='Slug', db_index=True),
            preserve_default=True,
        ),
    ]
