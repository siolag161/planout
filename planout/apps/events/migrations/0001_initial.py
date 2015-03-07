# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.fields
import django.core.files.storage
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
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
                ('status', models.CharField(default=b'scheduled', max_length=20, verbose_name='Event Status', choices=[(b'cancelled', 'cancelled'), (b'postponed', 'postponed'), (b'rescheduled', 'rescheduled'), (b'scheduled', 'scheduled')])),
                ('topic', models.CharField(blank=True, max_length=20, null=True, verbose_name='Event Topic', choices=[(b'business', 'business and professional'), (b'charity', 'charity and cause'), (b'culture', 'community and culture'), (b'family', 'family and education')])),
                ('category', models.CharField(blank=True, max_length=20, null=True, verbose_name='Event Category', choices=[(b'performance', 'concert or performance'), (b'conference', 'conference'), (b'gala', 'diner or gala'), (b'competition', 'game or competition')])),
                ('logo', core.fields.BaseImageField(storage=django.core.files.storage.FileSystemStorage(), max_length=1024, upload_to=core.fields.image_file_path, blank=True)),
                ('is_online', models.BooleanField(default=False, verbose_name="It's an online event")),
                ('organizer', models.ForeignKey(related_name='organized_events', verbose_name='Organizer', to='accounts.ProfessionalProfile')),
                ('poster', models.ForeignKey(related_name='posted_events', editable=False, to=settings.AUTH_USER_MODEL, verbose_name='Poster')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Occurrence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('end_time', models.DateTimeField(null=True, verbose_name='end', blank=True)),
                ('event', models.ForeignKey(related_name='occurrences', editable=False, to='events.Event', verbose_name='event')),
            ],
            options={
                'ordering': ('start_time', 'end_time'),
                'verbose_name': 'occurrence',
                'verbose_name_plural': 'occurrences',
            },
            bases=(models.Model,),
        ),
    ]
