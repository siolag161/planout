# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicuser',
            name='encoded_email',
            field=models.CharField(max_length=32, unique=True, null=True),
            preserve_default=True,
        ),
    ]
