# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='gmap_url',
            field=models.URLField(help_text=b'The official Google Place Page URL of this establishment.', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='icon_url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(help_text='Please enter the name', max_length=80, null=True, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='url',
            field=models.URLField(null=True, verbose_name='website', blank=True),
            preserve_default=True,
        ),
    ]
