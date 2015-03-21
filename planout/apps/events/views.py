# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms import ModelForm
# view imports
from django.contrib.gis.geos import GEOSGeometry
from django.views.generic import (View, FormView, DetailView, CreateView, RedirectView, UpdateView, ListView)

# Only authenticated users can access views using this.
from braces.views import (LoginRequiredMixin)
# form.

from django.shortcuts import render

from core.views import AjaxableFormViewMixin

from .adapter import EventAdapter
from .models import Event, ProfessionalProfile
from core.models import Location

from .forms import EventCreateForm

#from .

# Create your views here.

##########  BEGIN FORMS VIEWS  =========================================

#=======================================================================
class EventFormView(object):
    def get_adapter(self):
	return EventAdapter()

#=======================================================================
import logging
logger = logging.getLogger('werkzeug')


#=======================================================================
#  
#  EVENT CREATION
# 
#=======================================================================
def _extract_location(form):
    loc = Location()
    logger.critical(form.cleaned_data)

    for field in Location._meta.fields:
	fn = field.name	
	if fn in form.cleaned_data: # if the form has the same att
	     setattr(loc, fn, form.cleaned_data.get(fn))
    loc.set_coords( form.cleaned_data['longitude'], form.cleaned_data['latitude'])
    loc.save()
    
    return loc

#========================================================================
class EventCreateView(LoginRequiredMixin, EventFormView, AjaxableFormViewMixin, FormView):    
    template_name = 'events/create_form.html'
    form_class = EventCreateForm
    
    def get_success_url(self):
	return reverse_lazy("core:home")

    # add clean place_name
	
    def form_valid(self, form):
	from django.core.exceptions import ObjectDoesNotExist
	"""
	1. add organizer (via loggin-user)
	2. add location (if not existing)
	"""
	self.event = form.save(commit=False)
	self.event.location = _extract_location(form) # location set
	logger.warning("form_valid-event: should update the form to take into acc the organization id - then if not existing - create one. also the darm location & the heck fucking crop stuff")
	logger.critical(len(form.files))

	logo_file = None
	if form.files and forms.files[0]:
	    logo_file = form.files["logo"]	
	
	if self.request.user.is_authenticated():
	    user = self.request.user
	    profile = user.pro_profiles.first()
	    if not profile:
		profile = ProfessionalProfile.objects.create(owner = user, name=user.full_name, url="http://example.com", email=user.email)
	    else:
		logger.warning("should choose the default profile, not the first one")
	    self.event.organizer = profile
	    try:
		poster = self.event.poster
	    except ObjectDoesNotExist:
		self.event.poster = user
		
	    self.event.save()
	return super(EventCreateView,self).form_valid(form)

    ###
    def get_context_data(self, **kwargs):
	return super(EventCreateView,self).get_context_data(**kwargs)

##########  ENDS FORM VIEWS   ==========================================
