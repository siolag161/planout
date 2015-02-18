from django.core.cache import cache
from django.utils import six
from django.template.defaultfilters import slugify

#from .common import 

try:
    from django.utils.encoding import force_bytes
except ImportError:
    force_bytes = str


    
#==========================================================================
cached_funcs = set()

#================================	
def get_image_cache_key(user, width, height, prefix):
    """
    Returns a cache key consisten of a username and image size.
    """
    # encoded_email = get_encoded_email(user)
    key = six.u('%s_%s_%s') % (prefix, user.uuid, width, height)
    return six.u('%s_%s') % (slugify(key)[:100],
                             hashlib.md5(force_bytes(key)).hexdigest())
    
#================================
def cache_set(key, value):
    cache.set(key, value, config.AVATAR_CACHE_TIMEOUT)
    return value
    
#================================
def cache_result( default_width = 640, default_height=480 ):
    """
    Decorator to cache the result of functions that take a ``user`` and a
    ``size`` value.
    """
    def decorator(func):
        def cached_func(user, width, height):
            prefix = func.__name__
            cached_funcs.add(prefix)
            key = get_image_cache_key(user, width or default_width, height or default_height, prefix=prefix)
            result = cache.get(key)
            if result is None:
                result = func(user, width or default_width, height or default_height)
                cache_set(key, result)
            return result
        return cached_func
    return decorator
    
#================================
def invalidate_cache(user, width=None, height=None):
    """
    Function to be called when saving or changing an user's avatars.
    """
    #sizes = set(config.AVATAR_AUTO_GENERATE_SIZES)
    # if size is not None:
    #     sizes.add(size)
    for prefix in cached_funcs:
        #for size in sizes:
	if height and width:
	    cache.delete(get_cache_key(user, width, height, prefix))
