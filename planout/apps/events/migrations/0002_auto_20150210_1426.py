# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.fields
import django.core.files.storage
import django.utils.timezone
from django.conf import settings
import avatar.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Please enter the name', max_length=80, verbose_name='name')),
                ('slug', models.SlugField(null=True, verbose_name='Slug')),
                ('created', core.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', core.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('alternative_name', models.CharField(help_text='Please enter the alternative name', max_length=80, verbose_name='alternative name')),
                ('description', models.TextField(help_text='Please enter the description', verbose_name='desciption')),
                ('url', models.URLField()),
                ('status', models.CharField(default=b'scheduled', max_length=20, verbose_name='Event Status', choices=[(b'cancelled', 'cancelled'), (b'postponed', 'postponed'), (b'rescheduled', 'rescheduled'), (b'scheduled', 'scheduled')])),
                ('topic', models.CharField(max_length=20, null=True, verbose_name='Event Topic', choices=[(b'business', 'business and professional'), (b'charity', 'charity and cause'), (b'culture', 'community and culture'), (b'family', 'family and education')])),
                ('event_topic', models.CharField(max_length=20, null=True, verbose_name='Event Type', choices=[(b'business', 'business and professional'), (b'charity', 'charity and cause'), (b'culture', 'community and culture'), (b'family', 'family and education')])),
                ('age_range', models.CharField(max_length=6, verbose_name='Event age range')),
                ('organizer', models.ForeignKey(related_name='events', verbose_name='Organizer', to='events.Organization')),
                ('owner', models.ForeignKey(related_name='events', verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='EventCategory',
        ),
        migrations.DeleteModel(
            name='EventType',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='address',
        ),
        migrations.AddField(
            model_name='organization',
            name='email',
            field=models.EmailField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='logo',
            field=avatar.fields.AvatarField(storage=django.core.files.storage.FileSystemStorage(), max_length=1024, upload_to=avatar.fields.avatar_file_path, blank=True),
            preserve_default=True,
        ),
    ]
