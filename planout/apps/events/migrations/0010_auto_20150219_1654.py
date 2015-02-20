# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20150219_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='event',
            field=models.ForeignKey(related_name='occurences', editable=False, to='events.Event', verbose_name='event'),
            preserve_default=True,
        ),
    ]
