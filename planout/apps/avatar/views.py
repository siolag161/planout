import os
import uuid

from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import six
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .conf import settings
from avatar.forms import UploadAvatarForm
from .fields import AvatarField
# from avatar.signals import avatar_updated

from .util import (get_primary_avatar, get_default_avatar_url)
#                          get_user_model, get_user)

from core.utils.common import (get_user_model, get_user)
from core.fields import process_image_data
try:
    from PIL import Image
except ImportError:
    import Image
from django.utils import six

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from django.core.files.base import ContentFile
		   
import logging
logger = logging.getLogger('werkzeug')

def _get_next(request):
    """
    The part that's the least straightforward about views in this module is
    how they determine their redirects after they have finished computation.
    In short, they will try and determine the next place to go in the
    following order:
    1. If there is a variable named ``next`` in the *POST* parameters, the
       view will redirect to that variable's value.
    2. If there is a variable named ``next`` in the *GET* parameters,
       the view will redirect to that variable's value.
    3. If Django can determine the previous page from the HTTP headers,
       the view will redirect to that previous page.
    """
    next = request.POST.get('next', request.GET.get('next',
                            request.META.get('HTTP_REFERER', None)))
    if not next:
        next = request.path
    return next

    
@login_required
def add(request, extra_context=None, next_override='/',
        upload_form=UploadAvatarForm, *args, **kwargs):
    if extra_context is None:
	extra_context = {}
	
    avatar = get_primary_avatar(request.user)
    upload_avatar_form = upload_form(request.POST or None,
				     request.FILES or None,
				     user=request.user)

    #logger.critical(next_override)
    #logger.critical(_get_next(request))
    import json
    if request.method == "POST" and 'avatar' in request.FILES:
	if upload_avatar_form.is_valid():
	    user=request.user
	    # avatar = Avatar(user=request.user, primary=True)
	    image_file = request.FILES['avatar']
	    filename_parts = os.path.splitext(image_file.name)
	    extension = filename_parts[1]
	    
            filename = '%s%s' % (uuid.uuid4(), extension)    	    

	    logger.critical(json.loads(request.POST['avatar_data']))
	    params = json.loads(request.POST['avatar_data'])
	    params.update({"cropped":True})
	    image_file = process_image_data(image_file, **params)

	    #####
	    user.avatar.save(filename, image_file)
	    user.save()
	    messages.success(request, _("Successfully uploaded a new avatar."))
	    #logger.critical(next_override)
	    #return redirect(next_override or _get_next(request))
	    
    context = {
	'avatar': request.user.avatar,
	# 'avatars': avatars,
	'upload_avatar_form': upload_avatar_form,
	# 'next': next_override or _get_next(request),
    }
    context.update(extra_context)

    return render(request, 'avatar/avatar_form.html', context)
