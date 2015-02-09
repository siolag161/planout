import hashlib

try:
    from urllib.parse import urljoin, urlencode
except ImportError:
    from urlparse import urljoin
    from urllib import urlencode

from django import template
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.utils import six
from django.shortcuts import render

from avatar.conf import AvatarConf as config
from avatar.util import (get_primary_avatar, get_default_avatar_url,
                         cache_result, get_user_model, get_user, force_bytes)

register = template.Library()


@register.simple_tag
def avatar_url(user, size = config.AVATAR_DEFAULT_SIZE):
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

@register.simple_tag
def avatar(user, size=config.AVATAR_DEFAULT_SIZE, **kwargs):
    if not isinstance(user, get_user_model()):
        try:
            user = get_user(user)
            alt = six.text_type(user)
            url = avatar_url(user, size)
        except get_user_model().DoesNotExist:
            url =  get_default_avatar_url()
            alt = _("Default Avatar")
    else:
        alt = six.text_type(user)
        url = avatar_url(user, size)
    context = dict(kwargs, **{
        'user': user,
        'url': url,
        'alt': alt,
        'size': size,
    })
    return render_to_string('avatar/avatar_tag.html', context)


# @register.simple_tag
# def render_avatar_form(user, size=config.AVATAR_DEFAULT_SIZE, **kwargs):
#     if not isinstance(user, get_user_model()):
#         try:
#             user = get_user(user)
#             alt = six.text_type(user)
#             url = avatar_url(user, size)
#         except get_user_model().DoesNotExist:
#             url =  get_default_avatar_url()
#             alt = _("Default Avatar")
#     else:
#         alt = six.text_type(user)
#         url = avatar_url(user, size)
#     context = dict(kwargs, **{
#         'user': user,
#         'url': url,
#         'alt': alt,
#         'size': size,
#     })
#     return render_to_string('avatar/avatar_form.html', context)
