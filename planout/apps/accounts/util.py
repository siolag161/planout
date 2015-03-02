

from django.contrib.auth import get_user_model
from .conf import settings 


#===========================================================================
def get_primary_avatar(user):
    User = get_user_model()
    if not isinstance(user, User):	
        try:
            user = get_user(user)
        except User.DoesNotExist:
            return None	
    avatar = user.avatar
    if not avatar:
	avatar = None
    return avatar

def get_default_avatar_url():
    base_url = getattr(settings, 'MEDIA_URL', None)
    if not base_url:
        base_url = getattr(settings, 'STATIC_URL', '')

    # Don't use base_url if the default url starts with http:// of https://
    if settings.PROFILE_AVATAR_DEFAULT_URL.startswith(('http://', 'https://')):
        return settings.PROFILE_AVATAR_DEFAULT_URL
    # We'll be nice and make sure there are no duplicated forward slashes
    ends = base_url.endswith('/')

    begins = settings.PROFILE_AVATAR_DEFAULT_URL.startswith('/')
    if ends and begins:
        base_url = base_url[:-1]
    elif not ends and not begins:
        return '%s/%s' % (base_url, settings.PROFILE_AVATAR_DEFAULT_URL)

    return '%s%s' % (base_url, settings.PROFILE_AVATAR_DEFAULT_URL)

def get_avatar_url_or_defaul_url(user):
    avatar = get_primary_avatar(user)
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

