# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20150227_1414'),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='products',
            field=models.ManyToManyField(to='products.Product', verbose_name='Products', through='products.EventProduct'),
            preserve_default=True,
        ),
    ]
