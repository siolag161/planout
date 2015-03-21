# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150318_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='avenue_name',
            field=models.CharField(default='', max_length=40, verbose_name="Avenue's name"),
            preserve_default=False,
        ),
    ]
