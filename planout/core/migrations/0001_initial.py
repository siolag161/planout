# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import core.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Please enter the name', max_length=80, verbose_name='name')),
                ('slug', models.SlugField(null=True, verbose_name='Slug')),
                ('created', core.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', core.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('alternative_name', models.CharField(help_text='Please enter the alternative name', max_length=80, verbose_name='alternative name')),
                ('description', models.TextField(help_text='Please enter the description', verbose_name='desciption')),
                ('url', models.URLField()),
                ('owner', models.ForeignKey(related_name='basetypes', verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
