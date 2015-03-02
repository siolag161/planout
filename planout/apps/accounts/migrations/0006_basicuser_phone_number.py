# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20150301_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicuser',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
    ]
