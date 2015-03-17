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

from ..conf import settings as config

# from ..util import (get_primary_avatar, get_default_avatar_url,
#                          cache_result, get_user_model, get_user, force_bytes, get_avatar_url_or_defaul_url)

from ..util import ( get_primary_avatar, get_default_avatar_url,
                          get_avatar_url_or_defaul_url)
		    
from core.utils.common import ( get_user_model, get_user )
from core.utils.images import (force_bytes)
register = template.Library()

@register.simple_tag
def avatar_url(user, size = config.AVATAR_DEFAULT_SIZE):

   return get_avatar_url_or_defaul_url(user,size)
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
