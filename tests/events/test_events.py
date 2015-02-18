import os.path

from django.test import TestCase, modify_settings
from django.core.urlresolvers import reverse

from events.models import Organization, BasicUser, Event
from .factories import OrganizationFactory, UserFactory, EventFactory

from accounts.models import AvatarField
from avatar.util import (get_avatar_url_or_defaul_url, get_primary_avatar)
from avatar.conf import AvatarConf as config
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
class TestEventBasic(SluggedModelTests,TestCase):
    def setUp(self):
	self.user = UserFactory.create(username="bunbun", email="owner@bottofy.com")
	self.organization = OrganizationFactory.create(owner=self.user)
	
    def create_instance(self, **kwargs):
	return EventFactory.create(**kwargs)
	
    def create_new_user(self, **kwargs):
	return UserFactory.create()
	
	
#===============================================================================    
class EventCreate():
    def setUp(self):
	self.user = UserFactory.create(username="bunbun", email="owner@bottofy.com")
	self.organization = OrganizationFactory.create(owner=self.user)
	
    def test_create_new(self):
	event,created = get_or_create(name="event", organizer = self.organization)
	self.assertEqual(created, True)
	self.assertEqual(nbr_events(), 1)
	

    def test_create_check_defaul_values(self):
	event,created = get_or_create(name="event", organizer = self.organization)
	self.assertEqual(created, True)
	self.assertEqual(nbr_events(), 1)
	self.assertEqual( event.status, Event.EVENT_STATUS.scheduled )
	self.assertEqual( event.topic, Event.EVENT_TOPIC.business )
	self.assertEqual( event.category, Event.EVENT_CATEGORY.performance )

    def test_create_filter_age_range(self):
	event,created = get_or_create(name="event", organizer = self.organization)
	# event.set_age_range(12,25)
	self.assertEqual(event.age_range, (0,99))
	#logger.info(event.age_range)


    def test_create_json_mapping_api(self):
	event,created = get_or_create(name="event", organizer = self.organization)
	self.assertEqual(created, True)
#===============================================================================    
class EventUpdate(SluggedModelTests,TestCase):
    def setUp(self):
	self.user = UserFactory.create(username="bunbun", email="owner@bottofy.com")
	self.organization = OrganizationFactory.create(owner=self.user)
	
    def create_instance(self, **kwargs):
	return EventFactory.create(**kwargs)
	
    def create_new_user(self, **kwargs):
	return UserFactory.create()

#===============================================================================    
class EventDelete(SluggedModelTests,TestCase):
    def setUp(self):
	self.user = UserFactory.create(username="bunbun", email="owner@bottofy.com")
	self.organization = OrganizationFactory.create(owner=self.user)
	
    def create_instance(self, **kwargs):
	return EventFactory.create(**kwargs)
	
    def create_new_user(self, **kwargs):
	return UserFactory.create()

#===============================================================================    
class EventGet(SluggedModelTests,TestCase):
    def setUp(self):
	self.user = UserFactory.create(username="bunbun", email="owner@bottofy.com")
	self.organization = OrganizationFactory.create(owner=self.user)
	
    def create_instance(self, **kwargs):
	return EventFactory.create(**kwargs)
	
    def create_new_user(self, **kwargs):
	return UserFactory.create()

    
#===============================================================================
# http://nominatim.openstreetmap.org/reverse?format=json&lon=106.66577160358429&lat=10.768107861624031&zoom=18&addressdetails=1
def reverse_geocoding(coordinates):
    import requests

    base_url = "http://nominatim.openstreetmap.org/reverse"
    payload = {
	'format': 'json',
	'lat': coordinates[0],
	'lon': coordinates[1],
	'zoom': 18,
	'addressdetails': 1,
    }
    #logger.critical(payload)
    response = requests.get(base_url, params=payload)
    return response

class EventGeoLocation(SluggedModelTests,TestCase):
    
    def setUp(self):
	pass
	
    def create_instance(self, **kwargs):
	return EventFactory.create(**kwargs)
	
    def test_url(self):
	pass
	# from urltools import compare, normalize
	# event = self.create_instance()
	# response = reverse_geocoding(event.location['coordinates'])
	# streetmap_url = "http://nominatim.openstreetmap.org/reverse?format=json&"\
	#                      "lat=10.768107&lon=106.66577&zoom=18&addressdetails=1"
	# self.assertEqual(normalize(response.url), normalize(streetmap_url))
	# self.assertTrue(compare(response.url, streetmap_url))
	
