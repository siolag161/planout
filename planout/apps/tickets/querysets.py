from django.db import models
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManagerMixin
from prices import Price, PriceRange
from django.conf import settings

import logging
logger = logging.getLogger('werkzeug')

#==================================================================================================
class TicketQuerySet(QuerySet):
    pass

class TicketManager(models.Manager):

    def get_event_price_range(self, event, **kwargs):
	prices = [ ticket.get_price(**kwargs) for ticket in event.tickets.all()]	
	return PriceRange(min(prices), max(prices))
    
    def add_ticket_type(self, event, title, quantity, price = 0.0, **kwargs):
	"""
	@todo: discount & stuffs
	kwargs: currency / tax included v.v.
	"""
	currency = kwargs.get('currency', settings.DEFAULT_CURRENCY)
	ticket = self.create(event = event, name = title, stock = quantity, price = Price(price, currency=currency))
	return ticket


class PassThroughTicketManager(PassThroughManagerMixin, TicketManager):
    pass
