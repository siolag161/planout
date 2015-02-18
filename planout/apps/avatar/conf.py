from django.conf import settings
from PIL import Image
from appconf import AppConf


class AvatarConf(AppConf):
    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = 100
    AREA_WIDTH = 400
    AREA_HEIGHT = 250
    NO_RESIZE = False

    DEFAULT_SIZE = 80    
    RESIZE_METHOD = Image.ANTIALIAS
    STORAGE_DIR = 'avatars'
    STORAGE_PARAMS = {}
    GRAVATAR_FIELD = 'email'
    GRAVATAR_BASE_URL = 'http://www.gravatar.com/avatar/'
    GRAVATAR_BACKUP = True
    GRAVATAR_DEFAULT = None
    DEFAULT_URL = 'avatars/default/default_avatar.jpg'
    #MAX_AVATARS_PER_USER = 3
    MAX_SIZE = 1024 * 1024
    THUMB_FORMAT = 'JPEG'
    FORMAT = 'JPEG'

    THUMB_QUALITY = 85
    USERID_AS_USERDIRNAME = False
    HASH_FILENAMES = False
    HASH_USERDIRNAMES = False
    ALLOWED_FILE_EXTS = None
    CACHE_TIMEOUT = 60 * 60
    STORAGE = settings.DEFAULT_FILE_STORAGE
    CLEANUP_DELETED = False
    AUTO_GENERATE_SIZES = (DEFAULT_SIZE,)
    ALLOWED_MIMETYPES = []

    def configure_auto_generate_avatar_sizes(self, value):
        return value or getattr(settings, 'AVATAR_AUTO_GENERATE_SIZES',
                                (self.AVATAR_DEFAULT_SIZE,))

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
