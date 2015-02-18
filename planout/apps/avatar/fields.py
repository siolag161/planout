import os
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.core.files.base import ContentFile
from django.utils import six

from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class
from django.utils.translation import ugettext as _
from django.utils import six
from django.db.models import signals

#from .conf import AvatarConf as confi
from .conf import settings as config

# from .util import force_bytes, invalidate_cache, get_encoded_email
from core.utils.images import  force_bytes, invalidate_cache

from core.fields import BaseImageField

import forms

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from PIL import Image
except ImportError:
    import Image


avatar_storage = get_storage_class(config.AVATAR_STORAGE)(**config.AVATAR_STORAGE_PARAMS)

def avatar_file_path(user=None, filename=None, avatar = None, size=None, ext=None):
	
    tmppath = [config.AVATAR_STORAGE_DIR]
    userdirname = user.uuid
    # if config.AVATAR_USERID_AS_USERDIRNAME:
    #     userdirname = str(user.id)
    if config.AVATAR_HASH_USERDIRNAMES:
        tmp = hashlib.md5(userdirname).hexdigest()
        tmppath.extend([tmp[0], tmp[1], userdirname])
    else:
        tmppath.append(userdirname)
    if not filename:
        # Filename already stored in database
        filename = avatar.name
        if ext and config.AVATAR_HASH_FILENAMES:
            # An extension was provided, probably because the thumbnail
            # is in a different format than the file. Use it. Because it's
            # only enabled if AVATAR_HASH_FILENAMES is true, we can trust
            # it won't conflict with another filename
            (root, oldext) = os.path.splitext(filename)
            filename = root + "." + ext
    else:
        # File doesn't exist yet
        if config.AVATAR_HASH_FILENAMES:
            (root, ext) = os.path.splitext(filename)
            filename = hashlib.md5(force_bytes(filename)).hexdigest()
            filename = filename + ext

    if size:
        tmppath.extend(['resized', str(size)])
    tmppath.append(os.path.basename(filename))
    return os.path.join(*tmppath)

######################################################
class AvatarField(BaseImageField):
    def __init__(self, *args, **kwargs):
	
        # self.width = kwargs.pop('width', config.DEFAULT_WIDTH))
        # self.height = kwargs.pop('height', config.height)
	
	self.size = kwargs.get('size', config.AVATAR_DEFAULT_SIZE)	
        kwargs['upload_to'] = kwargs.get('upload_to', avatar_file_path)
	kwargs['storage'] = avatar_storage
	kwargs['blank'] = True
        super(AvatarField, self).__init__(*args, **kwargs)

    # def formfield(self, **kwargs):
    #     defaults = {'form_class': forms.AvatarField}
    #     # defaults['width'] = self.width
    #     # defaults['height'] = self.height
    #     defaults.update(kwargs)
    #     return super(AvatarField, self).formfield(**defaults)

#     def avatar_url(self, size):
#         return self.storage.url(self.avatar_name(size))

#     def get_absolute_url(self):
#         return self.avatar_url(config.AVATAR_DEFAULT_SIZE)

#     def avatar_name(self, user, size):
#         ext = find_extension(config.AVATAR_THUMB_FORMAT)
#         return avatar_file_path(
# 	    user = user,
#             avatar=self,
#             size=size,
#             ext=ext
#         )

# def find_extension(format):
#     format = format.lower()

#     if format == 'jpeg':
#         format = 'jpg'

#     return format
