from __future__ import unicode_literals
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible, smart_text
from django.db import models
from satchless.item import Item, StockedItem
from django_prices.models import PriceField
from django.core.validators import MinValueValidator
from decimal import Decimal

from django.utils.translation import pgettext_lazy
from satchless.item import ItemRange

from django.db import models

from core.models import (BaseType, TimeFramedModel, PostedModel)
#from events.models import Event #loading events
from core.loading import get_classes, get_model, get_class




from .querysets import (PassThroughTicketManager, TicketQuerySet)

class StockedProduct(models.Model, StockedItem):
    stock = models.IntegerField(pgettext_lazy('Product item field', 'stock'),
                                validators=[MinValueValidator(0)],
                                default=Decimal(1))
    class Meta:
        abstract = True
        app_label = 'tickets'

    def get_stock(self):
        return self.stock

class PricedProduct(models.Model):
    price = PriceField(
        pgettext_lazy('Product field', 'price'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=4)

    @property
    def is_free(self):
	return self.price.net == 0.0
    
    def get_price_per_item(self, discounts=None, **kwargs):
        if self.price:
            price = self.price
        # if discounts:
        #     discounts = list(get_product_discounts(self, discounts, **kwargs))
        #     if discounts:
        #         modifier = max(discounts)
        #         price += modifier
        return price

    class Meta:
        abstract = True
        app_label = 'tickets'

class Product(models.Model):   

    is_digital = models.BooleanField(_("Digital product?"), default = True)
    
    is_sellable = models.BooleanField(
        _("Is sellable?"), default=False, help_text=_(
            "This flag indicates if this product class can be sold"))

	
    def get_formatted_price(self, price):
        return "{0} {1}".format(price.gross, price.currency)

    def admin_get_price_min(self):
        price = self.get_price_range().min_price
        return self.get_formatted_price(price)
    admin_get_price_min.short_description = pgettext_lazy(
        'Product admin page', 'Minimum price')

    def admin_get_price_max(self):
        price = self.get_price_range().max_price
        return self.get_formatted_price(price)
    admin_get_price_max.short_description = pgettext_lazy(
        'Product admin page', 'Maximum price')
   
    class Meta:
	abstract = True
        app_label = 'tickets'

#============================================================================================
class Ticket(BaseType, TimeFramedModel, Product, PricedProduct, StockedProduct):
    event = models.ForeignKey( get_model('events', 'Event'), related_name = "tickets")
    objects = PassThroughTicketManager.for_queryset_class(TicketQuerySet)()

    @property
    def url_name(self):
	return "ticket:detail"
    # objects = 
    class Meta:
	unique_together = ("event", "name")
        app_label = 'tickets'
                                                
    
#===========================================================================================    
def get_event_price_range(event):
    return Ticket.objects.get_event_price_range(event)

from core.utils.db_check import auto_add_check_unique_together

#---------------------------------------------------------
auto_add_check_unique_together(Ticket)
