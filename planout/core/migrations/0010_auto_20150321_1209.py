# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150321_1039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='province',
        ),
        migrations.AlterField(
            model_name='location',
            name='city',
            field=models.CharField(help_text='Please enter the city', max_length=40, null=True, verbose_name='city/province'),
            preserve_default=True,
        ),
    ]
