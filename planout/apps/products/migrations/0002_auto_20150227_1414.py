# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(verbose_name='Event', to='events.Event')),
                ('product', models.ForeignKey(verbose_name='Product', to='products.Product')),
            ],
            options={
                'ordering': ['product', 'event'],
                'verbose_name': 'Product Event',
                'verbose_name_plural': 'Product Events',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='eventproduct',
            unique_together=set([('event', 'product')]),
        ),
    ]
