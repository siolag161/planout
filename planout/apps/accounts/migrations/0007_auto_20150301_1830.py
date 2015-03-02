# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_basicuser_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basicuser',
            old_name='birthday',
            new_name='birthdate',
        ),
    ]
