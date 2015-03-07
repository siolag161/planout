# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import core.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', core.fields.AutoSlugField(editable=False, max_length=250, blank=True, null=True, verbose_name='Slug', db_index=True)),
                ('created', core.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', core.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(help_text=b'The human-readable name for the place. For establishment results, this is usually the canonicalized business name.', max_length=255, null=True)),
                ('website', models.URLField(help_text=b"The authoritative website for this Place, such as a business' homepage.", null=True, blank=True)),
                ('formatted_address', models.CharField(help_text=b'The human-readable address of this place - composed of one or more address components.', max_length=255)),
                ('rating', models.DecimalField(help_text=b"Place's rating, from 1.0 to 5.0, based on user reviews.", null=True, max_digits=3, decimal_places=2, blank=True)),
                ('url', models.URLField(help_text=b'The official Google Place Page URL of this establishment.', null=True, blank=True)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(srid=4326, geography=True, verbose_name='longitude/latitude', blank=True)),
                ('placeId', models.CharField(help_text=b'Unique stable identifier denoting this place.', max_length=100, unique=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
