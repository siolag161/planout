import os
import uuid

from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import six
from django.utils.translation import ugettext as _

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .conf import settings
from avatar.forms import UploadAvatarForm
from .fields import AvatarField
# from avatar.signals import avatar_updated
from .util import (get_primary_avatar, get_default_avatar_url,
                         get_user_model, get_user)

@login_required
def add(request, extra_context=None, next_override=None,
        upload_form=UploadAvatarForm, *args, **kwargs):
    if extra_context is None:
        extra_context = {}
    # avatar, avatars = _get_avatars(request.user)
    upload_avatar_form = upload_form(request.POST or None,
                                     request.FILES or None,
                                     user=request.user)
    import logging
    log = logging.getLogger('werkzeug')
    
    if request.method == "POST" and 'avatar_file' in request.FILES:
        if upload_avatar_form.is_valid():
	    user=request.user
            # avatar = Avatar(user=request.user, primary=True)
            image_file = request.FILES['avatar_file']
            filename_parts = os.path.splitext(image_file.name)
            extension = filename_parts[1]
            filename = '%s%s' % (uuid.uuid4(), extension)
	    user.avatar.save(filename, image_file)
	    user.save(update_fields=['avatar'])
	    
            # avatar.avatar.save(filename, image_file)
            # avatar.save()
            messages.success(request, _("Successfully uploaded a new avatar."))
            # avatar_updated.send(sender=Avatar, user=request.user, avatar=avatar)

    context = {
        # 'avatar': avatar,
        # 'avatars': avatars,
        'upload_avatar_form': upload_avatar_form,
        # 'next': next_override or _get_next(request),
    }
    context.update(extra_context)
    
    return render(request, 'avatar/avatar_form.html', context)
