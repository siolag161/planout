# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import core.fields
import django.utils.timezone
import django.core.validators
import django_prices.models
import satchless.item


class Migration(migrations.Migration):

    dependencies = [
        ('events', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', core.fields.AutoSlugField(editable=False, max_length=250, blank=True, null=True, verbose_name='Slug', db_index=True)),
                ('created', core.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', core.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('start_time', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('end_time', models.DateTimeField(null=True, verbose_name='end', blank=True)),
                ('name', models.CharField(help_text='Please enter the name', max_length=80, verbose_name='name')),
                ('description', models.TextField(help_text='Please enter the description', null=True, verbose_name='description', blank=True)),
                ('url', models.URLField(null=True, verbose_name='website', blank=True)),
                ('stock', models.IntegerField(default=Decimal('1'), verbose_name='stock', validators=[django.core.validators.MinValueValidator(0)])),
                ('price', django_prices.models.PriceField(currency=b'VND', verbose_name='price', max_digits=12, decimal_places=4)),
                ('is_digital', models.BooleanField(default=True, verbose_name='Digital product?')),
                ('is_sellable', models.BooleanField(default=False, help_text='This flag indicates if this product class can be sold', verbose_name='Is sellable?')),
                ('event', models.ForeignKey(related_name='tickets', to='events.Event')),
            ],
            options={
            },
            bases=(models.Model, satchless.item.StockedItem),
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together=set([('event', 'name')]),
        ),
    ]
