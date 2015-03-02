from django.conf import settings
from PIL import Image
from appconf import AppConf


class AvatarConf(AppConf):
    AVATAR_DEFAULT_WIDTH = 100
    AVATAR_DEFAULT_HEIGHT = 100
    AVATAR_AREA_WIDTH = 400
    AVATAR_AREA_HEIGHT = 250
    AVATAR_AVATAR_NO_RESIZE = False

    AVATAR_DEFAULT_SIZE = 80    AVATAR_
    AVATAR_RESIZE_METHOD = Image.ANTIALIAS
    AVATAR_STORAGE_DIR = 'avatars'
    AVATAR_STORAGE_PARAMS = {}
    AVATAR_GRAVATAR_FIELD = 'email'
    AVATAR_GRAVATAR_BASE_URL = 'http://www.gravatar.com/avatar/'
    AVATAR_GRAVATAR_BACKUP = True
    AVATAR_GRAVATAR_DEFAULT = None
    AVATAR_DEFAULT_URL = 'avatars/default/default_avatar.jpg'
    AVATAR_MAX_SIZE = 1024 * 1024
    AVATAR_THUMB_FORMAT = 'JPEG'
    AVATAR_FORMAT = 'JPEG'

    AVATAR_THUMB_QUALITY = 85
    AVATAR_USERID_AS_USERDIRNAME = False
    AVATAR_HASH_FILENAMES = False
    AVATAR_HASH_USERDIRNAMES = False
    AVATAR_ALLOWED_FILE_EXTS = None
    AVATAR_CACHE_TIMEOUT = 60 * 60
    AVATAR_STORAGE = settings.DEFAULT_FILE_STORAGE
    AVATAR_CLEANUP_DELETED = False
    # AVATAR_AUTO_GENERATE_SIZES = (DEFAULT_SIZE,)
    AVATAR_ALLOWED_MIMETYPES = []

    # def configure_auto_generate_avatar_sizes(self, value):
    #     return value or getattr(settings, 'AVATAR_AUTO_GENERATE_SIZES',
    #                             (self.AVATAR_DEFAULT_SIZE,))

#     width = 100
#     height = 100

#     upload_to = 'avatars'
#     save_format = 'png'
#     save_quality = 90

#     select_area_width = 400
#     select_area_height = 250
settings_config = getattr(settings, 'AVATAR', {})

for key, value in settings_config.items():
    if key in AvatarConf.__dict__:
        setattr(AvatarConf, key, value)
    else:
        raise KeyError('Incorect option name of AVATAR in settings.py ({})'.format(key))
