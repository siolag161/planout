# -*- coding: utf-8 -*-
from django import template
from django.core.exceptions import ValidationError
from django.test import TestCase

from products import models as product_models
from events import models as event_models


from tests import factories

class TestEventProduct(TestCase):

    def setUp(self):
	self.ticket_product = factories.ProductClassFactory.create(name="TicketInfo", is_sellable=False)
	self.tickets = factories.ProductFactory.create_batch(20, product_class = self.ticket_product)
	self.events = factories.EventFactory.create_batch(20)
	
    def test_add_product_to_events(self):
	self.assertEqual(event_models.Event.objects.count(), 20)
	self.assertEqual(product_models.Product.objects.count(), 20)
	event = self.events[0]
	#ticket = self.tickets[0]

	for ticket in self.tickets:
	    event_models.EventProduct.objects.create(event=event,product = ticket)

	self.assertEqual(event.products.count(), 20)


