from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.conf import settings

from prices import Price, PriceRange
from tickets.models import Ticket, get_event_price_range

from tests.factories import (TicketFactory, EventFactory, UserFactory, ProProfileFactory)
from ..test_core.behaviors import SluggedModelTests
from .behaviors import *

import logging
logger = logging.getLogger('werkzeug')

class TicketTestCase(SluggedModelTests):
    def create_new_user(self, **kwargs):
	return UserFactory.create(**kwargs)

    def test_unique_together(self):
	self.event = EventFactory.create()
	t1 = self.event.add_ticket_type("VIP", 20, 100)
	self.assertRaises(IntegrityError, self.event.add_ticket_type, "VIP", 30, 200)


class FreeTicketTestCase(TicketTestCase, TestCase):
    def create_instance(self, **kwargs):
	self.currency = settings.DEFAULT_CURRENCY		
	return TicketFactory.create(price=Price(0, currency=self.currency), **kwargs)

    def setUp(self):
	self.obj = self.create_instance()
	self.assertEqual(self.obj.is_free, True)

    def test_creation(self):
	#self.ticket = TicketFactory.create(price=Price(0, currency=self.currency), **kwargs)	
	self.assertEqual(self.obj.is_sellable, False)
	self.assertEqual(self.obj.is_digital, True)
	# self.assertEqual(self.obj.is_free, True)
#==========================================================================================
class PaidTicketTestCase(TicketTestCase, TestCase):
    def create_instance(self, **kwargs):
	self.currency = settings.DEFAULT_CURRENCY		
	return TicketFactory.create(price=Price(20, currency=self.currency), **kwargs)

    def setUp(self):
	self.event = EventFactory.create()
	self.obj = self.create_instance(event = self.event)	
	self.assertEqual(self.obj.is_free, False)
	
    def test_creation(self):
	#self.ticket = TicketFactory.create(price=Price(0, currency=self.currency), **kwargs)	
	self.assertEqual(self.obj.is_sellable, False)
	self.assertEqual(self.obj.is_digital, True)
	self.assertEqual(self.obj.price.gross, 20)


    def test_get_price_range_unique_variant(self):
        'ItemRange.get_price_range() works and calls its items'
        self.assertEqual(get_event_price_range(self.event),
                         PriceRange(Price(20, currency=self.currency)))

    def test_get_price_range_multiple_variants(self):
        'ItemRange.get_price_range() works and calls its items'
	Ticket.objects.add_ticket_type(self.event, "VIP", 20, 100)
	Ticket.objects.add_ticket_type(self.event, "Discount", 200, 10)
	
        self.assertEqual(get_event_price_range(self.event),
                         PriceRange(Price(10, currency=self.currency), Price(100, currency=self.currency)) )
	Ticket.objects.add_ticket_type(self.event, "Super-VIP", 20, 400)

        self.assertEqual(get_event_price_range(self.event),
                         PriceRange(Price(10, currency=self.currency), Price(400, currency=self.currency)))

    # def test_get_price_range_on_empty(self):
    #     'ItemRange.get_price_range() raises an exception on an empty range'
    #     empty = EmptyRange()
    #     self.assertRaises(AttributeError, empty.get_price_range)
	


"""
test stock
"""
    
    
