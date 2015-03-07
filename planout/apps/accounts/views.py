# -*- coding: utf-8 -*-

import os
import uuid
import json

# Import the reverse lookup function
from django.contrib import messages
from django.utils.translation import ugettext as _

from django.core.urlresolvers import reverse
from django.forms import ModelForm
# view imports
from django.views.generic import (DetailView, RedirectView, UpdateView, ListView, FormView)
from core.views import AjaxableFormViewMixin
from core.fields import process_image_data

# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin
from core.utils.common import ( get_user_model, get_user )

# Import the form from users/forms.py
from .forms import UserEditForm, UserAvatarUploadForm
from .models import BasicUser

from .adapters import AccountAdapter
from .util import get_avatar_url_or_defaul_url
# Import the customized User mode
#==========================================================================================
import logging
logger = logging.getLogger('werkzeug')

class AccountFormViewMixin(object):
    def get_adapter(self):
	return AccountAdapter()

#======================================================================
class UserEditView( LoginRequiredMixin, AccountFormViewMixin,
		    AjaxableFormViewMixin, FormView ):
    model = BasicUser  
    template_name = 'accounts/user_edit_profile.html'
    form_class = UserEditForm

    def get_form(self, form_class):
        """
        Check if the user already saved contact details. If so, then show
        the form populated with those details, to let user change them.
        """
        try:
            user = get_user_model().objects.get(pk=self.request.user.pk)
            return form_class(instance=user, **self.get_form_kwargs())
        except get_user_model().DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
	form.save()
        return super(UserEditView, self).form_valid(form)

    def get_success_url(self):
	return reverse("profiles:edit_profile_uuid",
		       kwargs={"uuid": self.request.user.uuid})

    def get_context_data(self, **kwargs):
	ret = super(UserEditView, self).get_context_data(**kwargs)
	ret.update({
	    'avatar_url': get_avatar_url_or_defaul_url(self.request.user),
	    'avatar_update_form': UserAvatarUploadForm()
	})
	return ret
	
#======================================================================

class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False    
    def get_redirect_url(self):
	return reverse("profiles:detail",
		       kwargs={"username": self.request.user.username})

class UserListView(LoginRequiredMixin, ListView):
    model = BasicUser
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"

#================= BEGIN AVATAR ===============#
class AvatarAddView( LoginRequiredMixin, AccountFormViewMixin,
		     AjaxableFormViewMixin, FormView ):

    template_name = 'accounts/avatars/avatar_form.html'
    form_class = UserAvatarUploadForm
    
    def get_success_url(self):
    	return reverse("core:home")
	
    def get_form_kwargs(self):
	kwargs = super(AvatarAddView, self).get_form_kwargs()

	return kwargs

    def form_valid(self, form):	
	request = self.request	
	user = request.user
	image_file = request.FILES['avatar']
	filename_parts = os.path.splitext(image_file.name)
	extension = filename_parts[1]
	filename = '%s%s' % (uuid.uuid4(), extension)    	   

	params = json.loads(request.POST['avatar_data'])
	params.update({"cropped":True})
	image_file = process_image_data(image_file, **params)
	user.avatar.save(filename, image_file)
	user.save()
	messages.success(request, _("Successfully uploaded a new avatar."))
	
	return super(AvatarAddView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
	return super(AvatarAddView, self).post(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
	ret = super(AvatarAddView, self).get_context_data(**kwargs)
	ret.update({
	    'avatar_url': get_avatar_url_or_defaul_url(self.request.user),
	})
	return ret
