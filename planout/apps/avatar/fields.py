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

from .conf import AvatarConf as config

from .util import force_bytes, invalidate_cache, get_encoded_email
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
    userdirname = get_encoded_email(user)
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
    
class AvatarField(models.ImageField):
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

    def avatar_url(self, size):
        return self.storage.url(self.avatar_name(size))
	
    def save_form_data(self, instance, data):
        # if data and self.width and self.height:
	#print instance
	import logging
	log = logging.getLogger('werkzeug')
	log.warning("ca-vang-vang")
        file_ = data['file']
        if file_:
	    pass 
            image = Image.open(StringIO(file_.read()))
            image = image.crop(data['box'])
            image = image.resize( (self.size, self.size), Image.ANTIALIAS)

	    
	    img_data = six.BytesIO()
	    image.save(img_data, config.AVATAR_THUMB_FORMAT, quality=config.AVATAR_THUMB_QUALITY)
	    img_file = ContentFile(img_data.getvalue())
	    img_data = self.storage.save(self.avatar_name(instance,self.size), img_file)
            super(AvatarField, self).save_form_data(instance, img_data)
	    
            # content = StringIO()
            # image.save(content, config.AVATAR_THUMB_FORMAT, quality=config.AVATAR_THUMB_QUALITY)
	    #file = ContentFile(thumb.getvalue())
            # file_name = '{}.{}'.format(os.path.splitext(file_.name)[0], config.save_format)

            # # new_data = SimpleUploadedFile(file.name, content.getvalue(), content_type='image/' + config.save_format)
            # new_data = InMemoryUploasdedFile(content, None, file_name, 'image/' + config.save_format, len(content.getvalue()), None)



    def get_absolute_url(self):
        return self.avatar_url(config.AVATAR_DEFAULT_SIZE)

    def avatar_name(self, user, size):
        ext = find_extension(config.AVATAR_THUMB_FORMAT)
        return avatar_file_path(
	    user = user,
            avatar=self,
            size=size,
            ext=ext
        )

def find_extension(format):
    format = format.lower()

    if format == 'jpeg':
        format = 'jpg'

    return format
