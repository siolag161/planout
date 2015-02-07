# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import awesome_avatar.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_basicuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicuser',
            name='avatar',
            field=awesome_avatar.fields.AvatarField(default='', upload_to=b'avatars'),
            preserve_default=False,
        ),
    ]
