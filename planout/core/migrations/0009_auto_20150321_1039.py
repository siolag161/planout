# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_location_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='vicinity',
            new_name='formatted_address',
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(default='', help_text='Please enter the name', max_length=80, verbose_name='name'),
            preserve_default=False,
        ),
    ]
