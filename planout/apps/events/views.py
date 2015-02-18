# -*- coding: utf-8 -*-
# Import the reverse lookup function
from django.core.urlresolvers import reverse
from django.forms import ModelForm
# view imports
from django.views.generic import (View, FormView, DetailView, CreateView, RedirectView, UpdateView, ListView)

# Only authenticated users can access views using this.
from braces.views import (LoginRequiredMixin)
# form.

from django.shortcuts import render

from core.views import AjaxableFormViewMixin

from .adapter import EventAdapter
from .models import Event
from .forms import EventForm

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
    form_class = EventForm
    success_url = None    

    def form_valid(self, form):
	"""
	1. add organization (via loggin-user)
	2. add the age-range
	3. process the leaflet
	"""

	return super(EventCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
	return super(EventCreateView,self).get_context_data(**kwargs)

##########  ENDS FORM VIEWS   ==========================================
