# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms import ModelForm
# view imports
from django.views.generic import (View, FormView, DetailView, CreateView, RedirectView, UpdateView, ListView)

# Only authenticated users can access views using this.
from braces.views import (LoginRequiredMixin)
# form.

from django.shortcuts import render

from core.views import AjaxableFormViewMixin

from .adapter import EventAdapter
from .models import Event, Organization
from .forms import EventCreateForm


# Create your views here.

##########  BEGIN FORMS VIEWS  =========================================

#=======================================================================
class EventFormView(object):
    def get_adapter(self):
	return EventAdapter

#=======================================================================
import logging
logger = logging.getLogger('werkzeug')



class EventCreateView(LoginRequiredMixin, EventFormView, AjaxableFormViewMixin, FormView):
    
    template_name = 'events/create_form.html'
    form_class = EventCreateForm
    #success_url = reverse_lazy("core:home")

    def get_success_url(self):
	return reverse_lazy("core:home")
	
    def form_valid(self, form):
	"""
	1. add organization (via loggin-user)
	2. add the age-range
	3. process the leaflet
	"""
	self.object = form.save(commit=False)
	logger.warning("form_valid-event: should update the form to take into acc the organization id - then if not existing - create one. also the darm location & the heck fucking crop stuff")
	logo_file = form.files["logo"]
	if self.request.user.is_authenticated():
	    user = self.request.user
	    org = user.owned_organizations.first()
	    if not org:
		org = Organization.objects.create(owner = user, name=user.full_name, url="http://example.com", email=user.email)
		#logger.info(org.id)
		logger.info("new org: %s" % org.id)

	    else:
		logger.info("existing org: %s" % org.id)
	    self.object.organizer = org
	    self.object.logo.save("%s/embecun.jpg" %(user.uuid), logo_file)
	    self.object.address = {'type': 'Point', 'coordinates': [0, 0]}
	    self.object.save()
	return super(EventCreateView,self).form_valid(form)

    ###
    def get_context_data(self, **kwargs):
	return super(EventCreateView,self).get_context_data(**kwargs)

##########  ENDS FORM VIEWS   ==========================================
