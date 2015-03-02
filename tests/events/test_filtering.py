import os.path

from django.test import TestCase, modify_settings
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder

from events.models import ProfessionalProfile, BasicUser, Event, Occurrence
from tests.factories import ProProfileFactory, UserFactory, EventFactory


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

from prices import Price, PriceRange

logging.disable(logging.DEBUG)
from django.contrib.gis.geos import Point, Polygon

from django.utils import timezone

from tests.factories import get_tz_aware
# #######################################################################


# #######################################################################
# ### TEST CREATION OF OCCURRENCES ###
# #######################################################################
# class DateFilfteringTestCase(TestCase):
#     def create_instance(self, **kwargs):
#     	return EventFactory.create(**kwargs)
	
#     def setUp(self):
#     	#from datetime import timedelta
#     	EventFactory.reset_sequence(0, True)

#     	self.user = UserFactory.create(username="bunbun", email="owner@bottofy.com")
#     	self.organization = ProProfileFactory.create(owner=self.user)
#     	#self.event = self.create_instance(name="event", organizer = self.organization)
#     	self.events = EventFactory.create_batch(32)

#     	self.assertEqual(len(self.events), 32)
	
#     def test_next_week(self):
# 	for e in Event.objects.next_week():
# 	    logger.info("%s  -  %s " %(e.start_time, e.end_time))
#     	self.assertEqual(Event.objects.next_week().count(), 7)
#     	#EventFactory.reset_sequence(0, True)
#     	#EventFactory.create_batch(7)
#     	#self.assertEqual(Event.objects.next_week().count(), 7 + timezone.now().weekday())

#     def test_creation(self):	
#     	self.assertEqual(len(self.events), 32)

#     	for day in range(0,32):
#     	    self.assertEqual(Event.objects.by_day(now() + timedelta(days=day)).count(), 1)

#     	self.assertEqual(Event.objects.tomorrow().count(), 1)
#     	self.assertEqual(Event.objects.today().count(), 1)
#     	self.assertEqual(Event.objects.dayframe( now() - timedelta(hours = 2),
#     						 now() + timedelta(days=32)).count(), 32)

#     	self.assertEqual(Event.objects.datetimeframe( now() - timedelta(hours = 2),
#     						      now() + timedelta(days=32, hours=2)).count(), 32)

#     def test_this_week(self):
#     	self.assertEqual(Event.objects.this_week().count(), 7 - timezone.now().weekday())


#     def test_this_month(self):
# 	from dateutil.relativedelta import relativedelta

# 	today = timezone.now()
# 	last_day = today + relativedelta(day=1, months=+1, days=-1)
# 	delta_days = (last_day - today).days
#     	self.assertEqual(Event.objects.this_month().count(), delta_days + 1)

# #=============================================================================
# class PriceFilteringTestCase(TestCase):
#     def create_instance(self, **kwargs):
#     	return EventFactory.create(**kwargs)
	
#     def setUp(self):
# 	self.currency = settings.DEFAULT_CURRENCY
#     	EventFactory.reset_sequence(0, True)
#     	self.events = EventFactory.create_batch(5)
	
# 	for idx, e in enumerate(self.events):
# 	    for i in range(5):
# 		e.add_ticket_type("ticket-%s" % i, 5, 20+idx+i)

#     def test_tickets_added(self):
# 	from tickets.models import get_event_price_range
# 	check_quantity = all( [e.tickets.count() == 5] for e in self.events )
# 	self.assertTrue(check_quantity)
# 	#expected_range = PriceRange(Price(20, currency=self.currency), Price(24, currency=self.currency))
# 	check_prices = all( [get_event_price_range(e) ==
# 			     PriceRange(Price(20+idx, currency=self.currency),
# 					Price(24+idx, currency=self.currency))]
# 			     for  idx, e in enumerate(self.events) )
# 	self.assertTrue(check_prices)

#     def test_filter_by_price(self):
	
# 	from tickets.models import get_event_price_range
# 	price_range = PriceRange(Price(21, currency=self.currency), Price(27, currency=self.currency))
# 	filtered = Event.objects.within_price_range(21, 27, self.currency)

# 	self.assertEqual(filtered.count(), 5)
	
# 	filtered = Event.objects.within_price_range(26, 30, self.currency)
# 	self.assertEqual(filtered.count(), 3)
	
# 	filtered = Event.objects.within_price_range(28, 30, self.currency)
# 	self.assertEqual(filtered.count(), 1)


#     def test_free_ticket(self):
# 	f1 = Price(0, currency="VND")
# 	f2 = Price(0, currency="USD")
# 	self.assertEqual(f1.gross, f2.gross)

# 	event = self.create_instance()
# 	event.add_ticket_type("UCN", 20, 10, currency="VND")
# 	curr = event.tickets.first().price.currency
# 	self.assertEqual( curr, self.currency)
	
# 	filtered = Event.objects.is_free("VND")
# 	self.assertEqual(filtered.count(), 0)

# 	self.events[3].add_ticket_type("Free", 20, 0)
# 	filtered = Event.objects.is_free("VND")
# 	self.assertEqual(filtered.count(), 1)	
# 	self.assertEqual(filtered[0].pk, self.events[3].pk)


# #=============================================================================
# class StockFiltering(TestCase):
#     def create_instance(self, **kwargs):
#     	return EventFactory.create(**kwargs)
	
#     def setUp(self):
# 	self.currency = settings.DEFAULT_CURRENCY
#     	EventFactory.reset_sequence(0, True)

# 	self.nbr_events = 5
# 	self.events = EventFactory.create_batch(self.nbr_events)

# 	for idx, e in enumerate(self.events):
# 	    for i in range(self.nbr_events):
# 		e.add_ticket_type("ticket-%s" % i, 5, 20+idx+i)

#     def test_avai(self):
# 	self.assertEqual(self.nbr_events, Event.objects.is_available().count())	

# 	for e in self.events[0:3]:
# 	    for ticket in e.tickets.all():
# 		ticket.stock = 0		
# 		ticket.save()
		
# 	self.assertEqual(2, Event.objects.is_available().count())	

# class StockChainFiltering(TestCase):
	
#     def test_free_avai_ticket(self):
# 	events = EventFactory.create_batch(10)
# 	for idx, e in enumerate(events[0:5]):
# 	    if idx < 3:
# 		e.add_ticket_type("Free", 5, 0) # 3 free ticket
# 	    else:
# 		e.add_ticket_type("VIP", 10, 20) # 2 paid ticket

# 	for idx, e in enumerate(events[5:10]):

# 	    if idx < 3:
# 		e.add_ticket_type("Free", 0, 10) # 3 free ticket
# 	    else:
# 		e.add_ticket_type("VIP", 10, 0) # 2 paid ticket

# 	self.assertEqual(7, Event.objects.is_available().count())	
# 	self.assertEqual(5, Event.objects.is_free("VND").is_available().count())	
# 	self.assertEqual(5, Event.objects.within_price_range(10, 30, "VND").count())	

# #===================================================================================

class LocationBasedFiltering(TestCase):    
    def setUp(self):
	from django.contrib.gis.geos import fromstr
	self.poly = Polygon.from_bbox((54,104,59,109))
    	self.events = EventFactory.create_batch(10)
	self.pts = []
	for i, e in enumerate(self.events):
	    pt = fromstr('POINT(%s %s)' % (50+5,100+i))
	    e.location.coordinates = pt
	    e.location.save()

    def test_count(self):		
	self.assertEqual(Event.objects.count(), 10)
	filtered_pts = Event.objects.filter(location__coordinates__within=self.poly)
	self.assertEqual(filtered_pts.count(), 4)
