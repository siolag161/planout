from django.test import TestCase

#from products.models import ProductClass
from tests.factories import ProductClassFactory
from core.fields import NullCharField

class TestProductClassModel(TestCase):
    def setUp(self):
	self.tickets = ProductClassFactory.create(name="Ticket", is_sellable=False)


    def test_slug_is_auto_created(self):
        self.assertEqual('ticket', self.tickets.slug)

    def test_has_attribute_for_sellable(self):
	self.assertFalse(self.tickets.is_sellable)
	
    def test_has_attribute_for_digital(self):
	self.assertTrue(self.tickets.is_digital)
