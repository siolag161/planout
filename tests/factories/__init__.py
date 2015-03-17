# -*- coding: utf-8 -*-
import factory
import random
import string

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from datetime import datetime, timedelta
from django.utils import timezone
from accounts.models import ProfessionalProfile, BasicUser
from decimal import Decimal as D

from products.models import (Product, ProductClass, ProductAttribute,
			     AttributeOptionGroup, AttributeOption, ProductAttributeValue)

from stocks.models import StockRecord
import core.models as core_models

from events import models
from tickets.models import Ticket
from prices import Price

def random_string(length=10):
    return u''.join(random.choice(string.ascii_letters) for x in xrange(length))

def get_tz_aware(dt):
    if dt.tzinfo is None:
	return timezone.make_aware(dt, timezone.get_default_timezone())
    else:
	return dt
#=====================================================================================
class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = BasicUser
    username = factory.Sequence(lambda n: 'user' + str(n))
    email = factory.Sequence(lambda n: 'user_%s@gmail.com' % str(n))

class ProProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ProfessionalProfile
    owner = factory.SubFactory(UserFactory)
    name = "an organization"
    url = "http://orga.com"
    email = "bun@orga.com"
    class Meta:
	django_get_or_create = ('name', 'owner',)


#===================================
class LocationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = core_models.Location
    name = u'Trung Tâm Hội Nghị Tiệc Cưới Sài Gòn Phố Palace"'
    vicinity = u'1120 Võ Văn Kiệt, 6, 5'
    icon_url =  "http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png"
    coordinates = GEOSGeometry('POINT(10.750823 106.667536)')
    place_id = factory.Sequence(lambda n: 'ChIJO9XcB_kudTER5nTVkJMYa1U-%d' % n)


class ProductClassFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ProductClass
    is_digital = True
    is_sellable = False
    name = "tickets"

class ProductAttributeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ProductAttribute
    code = name = 'weight'
    product_class = factory.SubFactory(ProductClassFactory)
    type = "float"
    
class ProductFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Product
    #structure = Meta.model.STANDALONE
    upc = factory.Sequence(lambda n: '978080213020%d' % n)
    name = "A confederacy of dunces"
    product_class = factory.SubFactory(ProductClassFactory)

class AttributeOptionGroupFactory(factory.DjangoModelFactory):
    FACTORY_FOR = AttributeOptionGroup
    name = u'a group'

    
class AttributeOptionFactory(factory.DjangoModelFactory):
    option = factory.Sequence(lambda n: 'Option %d' % n)
    FACTORY_FOR = AttributeOption
    
class ProductAttributeValueFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ProductAttributeValue       
    attribute = factory.SubFactory(ProductAttributeFactory)
    product = factory.SubFactory(ProductFactory)

class EventFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Event
    organizer = factory.SubFactory(ProProfileFactory)
    poster = factory.SubFactory(UserFactory)
    status = models.Event.EVENT_STATUS.scheduled
    topic = models.Event.EVENT_TOPIC.business
    category = models.Event.EVENT_CATEGORY.performance
    age_range = (0,99)
    start_time = factory.Sequence(lambda n: get_tz_aware(timezone.now() + timedelta(days = n) ))
    end_time = factory.Sequence(lambda n: get_tz_aware(timezone.now() + timedelta(days = n, hours = 2) ))
    location = factory.SubFactory(LocationFactory) #GEOSGeometry('POINT(-120.18444970926208 50.65664762026928)')

    @classmethod
    def _setup_next_sequence(cls):      
	return getattr(cls, 'starting_seq_num', 0)

#=============================================================================
class StockRecordFactory(factory.DjangoModelFactory):
    product = factory.SubFactory(ProductFactory)
    partner = factory.SubFactory(ProProfileFactory)
    partner_sku = factory.Sequence(lambda n: 'unit%d' % n)
    price_currency = "GBP"
    price_excl_tax = D('9.99')
    num_in_stock = 100

    class Meta:
	model = StockRecord


#=============================================================================
class TicketFactory(factory.DjangoModelFactory):
    event = factory.SubFactory(EventFactory)
    name = 'Ticket'
    stock=10
    price=Price(10, currency=settings.DEFAULT_CURRENCY)
    #is_digital = True
    # poster = factory.SubFactory(UserFactory)
    class Meta:
	model = Ticket
