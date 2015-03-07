# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_basicuser_birthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicuser',
            name='description',
            field=models.TextField(help_text='Please enter the description', null=True, verbose_name='description', blank=True),
            preserve_default=True,
        ),
    ]
