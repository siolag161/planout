# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150228_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicuser',
            name='birthday',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
