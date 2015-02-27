# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import events.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='age_range',
            field=events.fields.AgeRangeField(default=b'0-130', null=True, verbose_name='Age range', blank=True),
            preserve_default=True,
        ),
    ]
