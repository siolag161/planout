# from django.conf import settings
# from django.forms import FileInput
# from django.template.loader import render_to_string


# from django import template
# from django.core.urlresolvers import reverse
# from django.template.loader import render_to_string
# from django.utils.translation import ugettext as _
# from django.utils import six

# from avatar.conf import AvatarConf as config
# from avatar.util import (get_primary_avatar, get_default_avatar_url,
#                          cache_result, get_user_model, get_user, force_bytes)

# from .conf import AvatarConf as config


# class AvatarWidget(FileInput):

#     def value_from_datadict(self, data, files, name):
#         value = {}
#         value['file'] = super(AvatarWidget, self).value_from_datadict(data, files, name)

#         x1 = data.get(name + '-x1', 0)
#         y1 = data.get(name + '-y1', 0)
#         x2 = data.get(name + '-x2', x1)
#         y2 = data.get(name + '-y2', y1)
#         ratio = float(data.get(name + '-ratio', 1))

#         box_raw = [x1, y1, x2, y2]
#         box = []

#         for coord in box_raw:
#             try:
#                 coord = int(coord)
#             except ValueError:
#                 coord = 0

#             if ratio > 1:
#                 coord = int(coord * ratio)
#             box.append(coord)

#         value['box'] = box
#         return value

#     def render(self, name, value, attrs=None):
	
# 	context = {
# 	    'preview_alt': "preview select area",
# 	    'size': config.AVATAR_DEFAULT_SIZE,
# 	    'select_width': config.AVATAR_AREA_WIDTH,
# 	    'select_height': config.AVATAR_AREA_HEIGHT} 
#         context['name'] = name
#         # context['config'] = config
#         # todo fix HACK
#         # context['STATIC_URL'] = AvatarConf.STATIC_URL
# 	context['name'] = name
#         # context['config'] = config
#         context['url'] = value.url if value and hasattr(value, 'url') else get_default_avatar_url()
#         context['id'] =  'id-' + name
#         return render_to_string('avatar/widget.html', context)
