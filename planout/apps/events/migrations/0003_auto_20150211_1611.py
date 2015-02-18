# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150210_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='Occurrence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('end_end', models.DateTimeField(null=True, verbose_name='end', blank=True)),
                ('event', models.ForeignKey(editable=False, to='events.Event', verbose_name='event')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='event',
            name='owner',
        ),
        migrations.AddField(
            model_name='event',
            name='end_end',
            field=models.DateTimeField(null=True, verbose_name='end', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(null=True, verbose_name='start', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='alternative_name',
            field=models.CharField(help_text='Please enter the alternative name', max_length=80, null=True, verbose_name='alternative name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(help_text='Please enter the description', null=True, verbose_name='desciption', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='alternative_name',
            field=models.CharField(help_text='Please enter the alternative name', max_length=80, null=True, verbose_name='alternative name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='description',
            field=models.TextField(help_text='Please enter the description', null=True, verbose_name='desciption', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='organization',
            name='url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
