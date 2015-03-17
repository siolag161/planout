from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from tests.factories import *

from products.models import (Product, ProductClass, ProductAttribute,  AttributeOption)

class TestTicketProductModel(TestCase):
    def setUp(self):
	self.ticket = ProductClassFactory.create(name="Ticket", is_sellable=False)
	self.seat_attribute = ProductAttributeFactory.create(product_class=self.tickets,
							     name="Seat number",
							     code='seat_number',
							     type='integer')
	Product.ENABLE_ATTRIBUTE_BINDING = True
	
    def tearDown(self):
	Product.ENABLE_ATTRIBUTE_BINDING = False
	ticket = ProductFactory.build(product_class=self.tickets,
				      name='blank ticket', upc=None)


    
