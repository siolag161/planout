import os.path

from django.test import TestCase, modify_settings
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder

from events.models import ProfessionalProfile, BasicUser, Event, Occurrence
from tests.factories import ProProfileFactory, UserFactory, EventFactory

from accounts.models import AvatarField
from avatar.util import (get_avatar_url_or_defaul_url, get_primary_avatar)
from avatar.conf import AvatarConf as config
from django.conf import settings
from django.contrib.auth import get_user_model

from django.utils.timezone import now
from datetime import datetime, timedelta, time

import dateutil.rrule as rrule

from ..test_core.forms import FormTests

from ..util import (get_login_redirect_url)

import json
from .test_events import TestEventBasic
from events.forms import EventCreateForm
from events.conf import settings as conf

import logging
logger = logging.getLogger('werkzeug')
from django.utils import timezone
#######################################################################
def get_tz_aware(dt):
    return timezone.make_aware(dt, timezone.get_current_timezone())

#######################################################################
### TEST CREATION OF OCCURRENCES ###
#######################################################################

class OccurrenceTestCase(TestCase):
    def create_instance(self, **kwargs):
	return EventFactory.create(**kwargs)
	
    def setUp(self):
	from datetime import timedelta
	self.user = UserFactory.create(username="bunbun", email="owner@bottofy.com")
	self.organization = ProProfileFactory.create(owner=self.user)
	self.event = self.create_instance(name="event", organizer = self.organization)

	self.assertTrue(self.event.start_time is not None)
	self.assertTrue(self.event.end_time is not None)
#=============================================================================
class OccurrenceCreationTests(OccurrenceTestCase):

    def test_decade_yearly(self):
	nbr_years = 10
	self.event.add_occurrences(get_tz_aware(datetime(2015,1,2)), get_tz_aware(datetime(2015,1,2,1)), freq=rrule.YEARLY, count=nbr_years)
	occs = list(self.event.occurrences.all())

        self.assertEqual(len(occs), nbr_years)
	for i in range(nbr_years):
	    o = occs[i]
            self.assertEqual(o.start_time.year, 2015 + i) 

    
    def test_create_25_daily(self):
	nbr_days = 25
	self.event.add_occurrences( get_tz_aware(datetime(2015,2,2)), get_tz_aware(datetime(2015,2,2,1)),
				    freq=rrule.DAILY, count=nbr_days )
	occs = list(self.event.occurrences.all())
        self.assertEqual(len(occs), nbr_days)
	for i in range(nbr_days):
	    o = occs[i]
            self.assertEqual(o.start_time.year, 2015)
            self.assertEqual(o.start_time.month, 2)
            self.assertEqual(o.start_time.day, i+1)
        self.assertEqual(self.event.daily_occurrences( get_tz_aware(datetime(2015,2,12))  ).count(), 1)

	e = self.create_instance()
	e.add_occurrences( get_tz_aware(datetime(2015,2,1)), get_tz_aware(datetime(2015,2,1,1)),
			    freq=rrule.DAILY, count=nbr_days )
	
	
        self.assertEqual(e.daily_occurrences( get_tz_aware(datetime(2015,2,11))  ).count(), 1)

    def test_weekly_occurrences(self):

	self.event.add_occurrences( get_tz_aware(datetime(2015,2,1,10,15)), get_tz_aware(datetime(2015,2,1,1,20)),
				    freq=rrule.WEEKLY, byweekday=(rrule.TU, rrule.TH),
				    until=get_tz_aware(datetime(2015,3,1,1)))

	occs = list(self.event.occurrences.all())
	self.assertEqual(self.event.occurrences.count(), 8)
	for i, day in zip(range(len(occs)), [3,5,10,12,17,19,24,26]):
            o = occs[i]
            self.assertEqual(day, o.start_time.day)
	    # self.assertEqual(o.end_time, get_tz_aware(datetime(2015,2,1,1,20))

	last_occ = self.event.occurrences.all().last()
	
	self.assertTrue(self.event.end_time >= last_occ.end_time)

    def test_upcoming_occurrences(self):
	right_now = datetime.now()
	one_hour_later = right_now + timedelta(hours = 2)
	one_week_later = right_now + timedelta(days = 7)
	self.event.add_occurrences( get_tz_aware(right_now), get_tz_aware(one_hour_later),
				    freq=rrule.WEEKLY, byweekday=(rrule.TU, rrule.TH),
				    until=get_tz_aware(one_week_later))

	#occs = list(self.event.occurrences.all())
	logger.critical(datetime.today().weekday())
	if abs(datetime.today().weekday() - 2) == 1:
	    self.assertEqual(self.event.occurrences.count(), 3)
	else:
	    self.assertEqual(self.event.occurrences.count(), 2)

	# for i, day in zip(range(len(occs)), [3,5,10,12,17,19,24,26]):
        #     o = occs[i]
        #     self.assertEqual(day, o.start_time.day)
	#     # self.assertEqual(o.end_time, get_tz_aware(datetime(2015,2,1,1,20))

	# occs = list(self.event.upcoming_occurrences())
        # self.assertEqual(len(occs), 2)
	# for i, day in zip(range(len(occs)), [24,26]):
        #     o = occs[i]
        #     self.assertEqual(day, o.start_time.day)

	# last_occ = self.event.occurrences.all().last()
	# self.assertTrue(self.event.end_time >= last_occ.end_time)
	
        # self.assertIsNotNone(self.event.next_occurrence())
        # self.assertIsNotNone(self.event.next_occurrence().start_time.day, 24)


#=============================================================================
class OccurrencUpdateTests(OccurrenceTestCase):
    pass

	
	
#######################################################################
### TEST UPCOMING & PAST OF OCCURRENCES ###
#######################################################################
