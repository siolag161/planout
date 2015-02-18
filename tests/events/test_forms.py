import os.path

from django.test import TestCase, modify_settings
from django.core.urlresolvers import reverse

from events.models import Organization, BasicUser, Event
from events.forms import EventForm
from .factories import OrganizationFactory, UserFactory, EventFactory

from django.conf import settings
from django.contrib.auth import get_user_model 

import settings as local_settings
from ..test_core.behaviors import  OwnedModelTests,SluggedModelTests
 
from ..util import (get_login_redirect_url)

import logging
logger = logging.getLogger('werkzeug')

#####################################################

def get_or_create(**kwargs):
    try:
	event = Event.objects.get(**kwargs)
	created = False 
    except Event.DoesNotExist:
	event = EventFactory.create(**kwargs)
	created = True
    return event, created

def nbr_events():
    return Event.objects.count()

#########################################################################
class TestBasicEventForm(TestCase):
    def setUp(self):
	pass

    def get_form_data(self, **kwargs):	
	return {}

    def create_form_instance(self, **kwargs):	
        form = MyForm(data=self.get_form_data(**kwargs))
        self.assertEqual(form.is_valid(), True)
	
    def test_event_create_form(self):
	pass
	# self.assertTrue(False)
	
#===============================================================================    
