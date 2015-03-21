# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_location_coordinates'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='url',
            new_name='website_url',
        ),
        migrations.RemoveField(
            model_name='location',
            name='icon_url',
        ),
        migrations.AddField(
            model_name='location',
            name='city',
            field=models.CharField(help_text='Please enter the city', max_length=40, null=True, verbose_name='city'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='country_code',
            field=models.CharField(max_length=3, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='district',
            field=models.CharField(help_text='Please enter the district', max_length=40, null=True, verbose_name='district'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='province',
            field=models.CharField(max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='route',
            field=models.CharField(help_text='Please enter the street name', max_length=40, null=True, verbose_name='street name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.CharField(max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='street_number',
            field=models.CharField(help_text='Please enter the street number', max_length=40, null=True, verbose_name='street number'),
            preserve_default=True,
        ),
    ]
