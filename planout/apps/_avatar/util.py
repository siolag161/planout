import hashlib

from django.core.cache import cache
from django.utils import six
from django.template.defaultfilters import slugify
import base64
try:
    from django.utils.encoding import force_bytes
except ImportError:
    force_bytes = str

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    def get_user_model():
        return User
    custom_user_model = False
else:
    custom_user_model = True

#from .conf import AvatarConf as config
from .conf import settings as config

# from .conf import settings

# cached_funcs = set()

# def base64_normalize(encoded_url):
#     paddings = (4 - len(encoded_url)%4)
#     encoded_url += "=" * paddings
#     return encoded_url

# def base64_decode_url(encoded_url):
#     encoded_url = base64_normalize(encoded_url)
#     return base64.urlsafe_b64decode(encoded_url)

# def url_safe_normalize(encoded_url):
#     encoded_url = encoded_url.replace("=","")
#     return encoded_url
    
# def base64_encode_url(string):
#     encoded_url = base64.urlsafe_b64encode(string)
#     return url_safe_normalize(encoded_url)

# # def decode_string(encoded_string):
# #     return base64.urlsafe_b64decode(encoded_string)
    
# #####
# def get_encoded_email(user):
#     """ Return username of a User instance """
#     if hasattr(user, 'encoded_email'):
# 	return user.encoded_email
#     else:
#         return base64_encode_url(user.email)


# def get_user(username):
#     """ Return user from a username/ish identifier """
#     if custom_user_model:
#         return get_user_model().objects.get_by_natural_key(username)
#     else:
#         return get_user_model().objects.get(username=username)


# def get_cache_key(user, size, prefix):
#     """
#     Returns a cache key consisten of a username and image size.
#     """
#     encoded_email = get_encoded_email(user)
#     key = six.u('%s_%s_%s') % (prefix, encoded_email, size)
#     return six.u('%s_%s') % (slugify(key)[:100],
#                              hashlib.md5(force_bytes(key)).hexdigest())


# def cache_set(key, value):
#     cache.set(key, value, config.AVATAR_CACHE_TIMEOUT)
#     return value


# def cache_result(default_size=config.AVATAR_DEFAULT_SIZE):
#     """
#     Decorator to cache the result of functions that take a ``user`` and a
#     ``size`` value.
#     """
#     def decorator(func):
#         def cached_func(user, size=None):
#             prefix = func.__name__
#             cached_funcs.add(prefix)
#             key = get_cache_key(user, size or default_size, prefix=prefix)
#             result = cache.get(key)
#             if result is None:
#                 result = func(user, size or default_size)
#                 cache_set(key, result)
#             return result
#         return cached_func
#     return decorator


# def invalidate_cache(user, size=None):
#     """
#     Function to be called when saving or changing an user's avatars.
#     """
#     sizes = set(config.AVATAR_AUTO_GENERATE_SIZES)
#     if size is not None:
#         sizes.add(size)
#     for prefix in cached_funcs:
#         for size in sizes:
#             cache.delete(get_cache_key(user, size, prefix))


def get_default_avatar_url():
    base_url = getattr(config, 'MEDIA_URL', None)
    if not base_url:
        base_url = getattr(config, 'STATIC_URL', '')

    # Don't use base_url if the default url starts with http:// of https://
    if config.AVATAR_DEFAULT_URL.startswith(('http://', 'https://')):
        return config.AVATAR_DEFAULT_URL
    # We'll be nice and make sure there are no duplicated forward slashes
    ends = base_url.endswith('/')

    begins = config.AVATAR_DEFAULT_URL.startswith('/')
    if ends and begins:
        base_url = base_url[:-1]
    elif not ends and not begins:
        return '%s/%s' % (base_url, config.AVATAR_DEFAULT_URL)

    return '%s%s' % (base_url, config.AVATAR_DEFAULT_URL)


def get_primary_avatar(user, size=config.AVATAR_DEFAULT_SIZE):
    import logging
    logger = logging.getLogger('werkzeug')

    User = get_user_model()
    if not isinstance(user, User):	
        try:
            user = get_user(user)
        except User.DoesNotExist:
            return None	
    avatar = user.avatar
    if not avatar:
	avatar = None
    # if avatar:
    # 	if not avatar.thumbnail_exists(size):
    # 	    avatar.create_thumbnail(size)
    return avatar


def get_avatar_url_or_defaul_url(user, size=config.AVATAR_DEFAULT_SIZE):
    avatar = get_primary_avatar(user, size=size)
    if avatar:
        return avatar.url
    # if settings.AVATAR_GRAVATAR_BACKUP: @todo: deal with default gravatar stuff
    #     params = {'s': str(size)}
    #     if settings.AVATAR_GRAVATAR_DEFAULT:
    #         params['d'] = settings.AVATAR_GRAVATAR_DEFAULT
    #     path = "%s/?%s" % (hashlib.md5(force_bytes(user.email)).hexdigest(),
    #                        urlencode(params))
    #     return urljoin(settings.AVATAR_GRAVATAR_BASE_URL, path)

    return get_default_avatar_url()
