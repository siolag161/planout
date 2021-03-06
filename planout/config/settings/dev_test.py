import django
from .dev import *

INSTALLED_APPS += (
    'tests.test_core',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',	
        'NAME': 'planout_test',
        'USER': 'dev',
        'PASSWORD': 'dev',
        'HOST': 'localhost', 
        'PORT': '5432', 
    } 
}

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    # These are allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    "extensions.allauth.account.context_processors.account",

)

SITE_ID = 1
SECRET_KEY = 'something-something'
STATIC_URL = '/site_media/static/'


AVATAR_ALLOWED_FILE_EXTS  = ('.jpg', '.png', '.jpeg')
AVATAR_MAX_SIZE = 1024 * 1024


MEDIA_ROOT = '/tmp/media/'
