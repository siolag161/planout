# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_basicuser_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicuser',
            name='modified',
            field=core.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='basicuser',
            name='date_joined',
            field=core.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='date joined', editable=False),
            preserve_default=True,
        ),
    ]
