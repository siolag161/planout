# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150212_0750'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_topic',
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Event Category', choices=[(b'performance', 'concert or performance'), (b'conference', 'conference'), (b'gala', 'diner or gala'), (b'competition', 'game or competition')]),
            preserve_default=True,
        ),
    ]
