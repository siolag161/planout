# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import core.fields
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('events', '__first__'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('option', models.CharField(max_length=255, verbose_name='Option')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Attribute option',
                'verbose_name_plural': 'Attribute options',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AttributeOptionGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Attribute option group',
                'verbose_name_plural': 'Attribute option groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(verbose_name='Event', to='events.Event')),
            ],
            options={
                'ordering': ['product', 'event'],
                'verbose_name': 'Product Event',
                'verbose_name_plural': 'Product Events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', core.fields.AutoSlugField(editable=False, max_length=250, blank=True, null=True, verbose_name='Slug', db_index=True)),
                ('created', core.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', core.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(help_text='Please enter the name', max_length=80, verbose_name='name')),
                ('description', models.TextField(help_text='Please enter the description', null=True, verbose_name='description', blank=True)),
                ('url', models.URLField(null=True, verbose_name='website', blank=True)),
                ('upc', core.fields.NullCharField(max_length=64, help_text='Universal Product Code (UPC) is an identifier for a product which is not specific to a particular  supplier. Eg an ISBN for a book.', unique=True, verbose_name='UPC')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('code', models.SlugField(max_length=128, verbose_name='Code', validators=[django.core.validators.RegexValidator(regex=b'^[a-zA-Z\\-_][0-9a-zA-Z\\-_]*$', message="Code can only contain the letters a-z, A-Z, digits, minus and underscores, and can't start with a digit")])),
                ('type', models.CharField(default=b'text', max_length=20, verbose_name='Type', choices=[(b'text', 'Text'), (b'integer', 'Integer'), (b'boolean', 'True / False'), (b'float', 'Float'), (b'richtext', 'Rich Text'), (b'date', 'Date'), (b'option', 'Option'), (b'entity', 'Entity'), (b'file', 'File'), (b'image', 'Image')])),
                ('required', models.BooleanField(default=False, verbose_name='Required')),
                ('option_group', models.ForeignKey(blank=True, to='products.AttributeOptionGroup', help_text='Select an option group if using type "Option"', null=True, verbose_name='Option Group')),
            ],
            options={
                'ordering': ['code'],
                'abstract': False,
                'verbose_name': 'Product attribute',
                'verbose_name_plural': 'Product attributes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductAttributeValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value_text', models.TextField(null=True, verbose_name='Text', blank=True)),
                ('value_integer', models.IntegerField(null=True, verbose_name='Integer', blank=True)),
                ('value_boolean', models.NullBooleanField(verbose_name='Boolean')),
                ('value_float', models.FloatField(null=True, verbose_name='Float', blank=True)),
                ('value_richtext', models.TextField(null=True, verbose_name='Richtext', blank=True)),
                ('value_date', models.DateField(null=True, verbose_name='Date', blank=True)),
                ('entity_object_id', models.PositiveIntegerField(null=True, editable=False, blank=True)),
                ('attribute', models.ForeignKey(verbose_name='Attribute', to='products.ProductAttribute')),
                ('entity_content_type', models.ForeignKey(blank=True, editable=False, to='contenttypes.ContentType', null=True)),
                ('product', models.ForeignKey(related_name='attribute_values', verbose_name='Product', to='products.Product')),
                ('value_option', models.ForeignKey(verbose_name='Value option', blank=True, to='products.AttributeOption', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Product attribute value',
                'verbose_name_plural': 'Product attribute values',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', core.fields.AutoSlugField(editable=False, max_length=250, blank=True, null=True, verbose_name='Slug', db_index=True)),
                ('created', core.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', core.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(help_text='Please enter the name', max_length=80, verbose_name='name')),
                ('description', models.TextField(help_text='Please enter the description', null=True, verbose_name='description', blank=True)),
                ('url', models.URLField(null=True, verbose_name='website', blank=True)),
                ('is_digital', models.BooleanField(default=True, verbose_name='Digital product?')),
                ('is_sellable', models.BooleanField(default=False, help_text='This flag indicates if this product class can be sold', verbose_name='Is sellable?')),
                ('track_stock', models.BooleanField(default=True, verbose_name='Track stock levels?')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'Product class',
                'verbose_name_plural': 'Product classes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='productattributevalue',
            unique_together=set([('attribute', 'product')]),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='product_class',
            field=models.ForeignKey(related_name='attributes', verbose_name='Product type', blank=True, to='products.ProductClass', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(help_text='A product attribute is something that this product may have, such as a size, as specified by its class', to='products.ProductAttribute', verbose_name='Attributes', through='products.ProductAttributeValue'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='product_class',
            field=models.ForeignKey(related_name='products', on_delete=django.db.models.deletion.PROTECT, verbose_name='Product type', to='products.ProductClass', help_text='Choose what type of product this is', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='eventproduct',
            name='product',
            field=models.ForeignKey(verbose_name='Product', to='products.Product'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='eventproduct',
            unique_together=set([('event', 'product')]),
        ),
        migrations.AddField(
            model_name='attributeoption',
            name='group',
            field=models.ForeignKey(related_name='options', verbose_name='Group', to='products.AttributeOptionGroup'),
            preserve_default=True,
        ),
    ]
