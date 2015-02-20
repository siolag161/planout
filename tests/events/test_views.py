import os.path

from django.test import TestCase, modify_settings
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder

from events.models import Organization, BasicUser, Event
from .factories import OrganizationFactory, UserFactory, EventFactory

from accounts.models import AvatarField
from avatar.util import (get_avatar_url_or_defaul_url, get_primary_avatar)
from avatar.conf import AvatarConf as config
from django.conf import settings
from django.contrib.auth import get_user_model

from django.utils.timezone import now
from datetime import datetime, timedelta, time

from ..test_core.behaviors import OwnedModelTests, SluggedModelTests, AuthentificatedMixin
from ..test_core.forms import FormTests

from ..util import (get_login_redirect_url)

import json

import logging
logger = logging.getLogger('werkzeug')


from .test_events import TestEventBasic
from events.forms import EventCreateForm

EVENT_CREATE_URL = reverse('events:event_create')
def create_helper(o, filename, **kwargs):
    f = open(os.path.join(o.testdatapath, filename), "rb")
    params = {
	'logo': f,
    }
    params.update(**kwargs)

    #logger.info(params)
    response = o.client.post(EVENT_CREATE_URL, params, follow=True)
    f.close()
    return response


class TestNonAuthenticated(TestEventBasic):
    def setUp(self):
	#self.settings = local_settings
	self.username = 'testuser'
	self.password = 'testpass'
	self.email = 'bunbun@gmail.com'
	self.testdatapath = os.path.join(os.path.dirname(__file__), "data")

	User = get_user_model()
	self.user = User.objects.create_user( email=self.email, password=self.password)
	logged_in = self.client.login(username = self.username, email = self.email, password = "")
	self.assertFalse(logged_in)

    def test_login(self):
	self.assertEqual(self.user.email, "bunbun@gmail.com")

    def test_uploadNormal(self):
    	response = create_helper(self, "default_avatar.jpg")
        self.assertEqual(response.status_code, 200)
	self.assertRedirects(response, get_login_redirect_url(EVENT_CREATE_URL) )

##############


class DefaultCreateAuthenticatedTestCase(FormTests, TestCase, AuthentificatedMixin):
    form_class = EventCreateForm
    def get_form_data(self):
	data = {
	    'name': "The very event",
	    'start_time': "2015-02-06 18:07",
	    'end_time': "2015-02-06 20:07",
	    'url': "http://google.com",
	    'is_online': True,
	    "category": Event.EVENT_CATEGORY.performance,
	    'topic': Event.EVENT_TOPIC.business,  
	}
	return data
    
    def setUp(self):
	#self.settings = local_settings
	self.testdatapath = os.path.join(os.path.dirname(__file__), "data")
	self.user = self.create_user()	

    def test_create(self):
	response = create_helper(self, "default_avatar.jpg", **self.get_form_data())
        self.assertEqual( response.status_code, 200 )
	events = Event.objects.all()
	self.assertEqual(Event.objects.count(), 1)


    def test_create_existing_organization(self):
	orga = OrganizationFactory.create(owner = self.user)
	response = create_helper(self, "default_avatar.jpg", **self.get_form_data())
        self.assertEqual( response.status_code, 200 )
	self.assertEqual(Event.objects.count(), 1)
	event = Event.objects.first()
	self.assertEqual(orga.id, event.organizer.id)

    
