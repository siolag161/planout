# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_delete_agerange'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=djgeojson.fields.PointField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='event_topic',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Event Type', choices=[(b'business', 'business and professional'), (b'charity', 'charity and cause'), (b'culture', 'community and culture'), (b'family', 'family and education')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(related_name='organized_events', verbose_name='Organizer', to='events.Organization'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='topic',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Event Topic', choices=[(b'business', 'business and professional'), (b'charity', 'charity and cause'), (b'culture', 'community and culture'), (b'family', 'family and education')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='owner',
            field=models.ForeignKey(related_name='owned_organizations', verbose_name='Owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
