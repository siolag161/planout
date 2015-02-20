import os.path

from django.test import TestCase, modify_settings
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder

from events.models import Organization, BasicUser, Event, Occurrence
from .factories import OrganizationFactory, UserFactory, EventFactory

from accounts.models import AvatarField
from avatar.util import (get_avatar_url_or_defaul_url, get_primary_avatar)
from avatar.conf import AvatarConf as config
from django.conf import settings
from django.contrib.auth import get_user_model

from django.utils.timezone import now
from datetime import datetime, timedelta, time

import dateutil.rrule as rrule


from ..test_core.behaviors import OwnedModelTests, SluggedModelTests, AuthentificatedMixin
from ..test_core.forms import FormTests

from ..util import (get_login_redirect_url)

import json
from .test_events import TestEventBasic
from events.forms import EventCreateForm
from events.conf import settings as conf

import logging
logger = logging.getLogger('werkzeug')

logging.disable(logging.DEBUG)

from django.utils import timezone

from .factories import get_tz_aware
#######################################################################


#######################################################################
### TEST CREATION OF OCCURRENCES ###
#######################################################################
class DateFilfteringTestCase(TestCase):
    def create_instance(self, **kwargs):
    	return EventFactory.create(**kwargs)
	
    def setUp(self):
    	#from datetime import timedelta
    	EventFactory.reset_sequence(0, True)

    	self.user = UserFactory.create(username="bunbun", email="owner@bottofy.com")
    	self.organization = OrganizationFactory.create(owner=self.user)
    	#self.event = self.create_instance(name="event", organizer = self.organization)
    	self.events = EventFactory.create_batch(32)

    	self.assertEqual(len(self.events), 32)
	
    def test_next_week(self):
	for e in Event.objects.next_week():
	    logger.info("%s  -  %s " %(e.start_time, e.end_time))
    	self.assertEqual(Event.objects.next_week().count(), 7)
    	#EventFactory.reset_sequence(0, True)
    	#EventFactory.create_batch(7)
    	#self.assertEqual(Event.objects.next_week().count(), 7 + timezone.now().weekday())

    def test_creation(self):	
    	self.assertEqual(len(self.events), 32)

    	for day in range(0,32):
    	    self.assertEqual(Event.objects.by_day(now() + timedelta(days=day)).count(), 1)

    	self.assertEqual(Event.objects.tomorrow().count(), 1)
    	self.assertEqual(Event.objects.today().count(), 1)
    	self.assertEqual(Event.objects.dayframe( now() - timedelta(hours = 2),
    						 now() + timedelta(days=32)).count(), 32)

    	self.assertEqual(Event.objects.datetimeframe( now() - timedelta(hours = 2),
    						      now() + timedelta(days=32, hours=2)).count(), 32)

    def test_this_week(self):
    	self.assertEqual(Event.objects.this_week().count(), 7 - timezone.now().weekday())


    def test_this_month(self):
	from dateutil.relativedelta import relativedelta

	today = timezone.now()
	last_day = today + relativedelta(day=1, months=+1, days=-1)
	delta_days = (last_day - today).days
    	self.assertEqual(Event.objects.this_month().count(), delta_days + 1)

#=============================================================================
