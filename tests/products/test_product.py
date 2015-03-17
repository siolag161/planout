from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from tests.factories import (ProductFactory, ProductAttributeFactory,ProductAttributeValueFactory,
			ProductClassFactory, AttributeOptionGroupFactory,
			AttributeOptionFactory, ProProfileFactory)

from products.models import (Product,
			     ProductClass,
			     ProductAttribute,
			     AttributeOption)
from stocks import prices

class TestProductModel(TestCase):
    def setUp(self):
	self.tickets = ProductClassFactory.create(name="Ticket", is_sellable=False)
	self.seat_attribute = ProductAttributeFactory.create(product_class=self.tickets,
							     name="Seat number",
							     code='seat_number',
							     type='integer')


    def test_create_products_with_attributes(self):
        ticket = ProductFactory.build( upc='1234',
					product_class=self.tickets,
					name='testing')
        ticket.attr.seat_number = 100
	ticket.attr.alibaba = 100
        ticket.save()
	ticket = Product.objects.get(pk=ticket.pk)
	self.assertEqual(ticket.attr.seat_number, 100)
	self.assertFalse(hasattr(ticket.attr, "alibaba"))
	
    def test_none_upc_is_represented_as_empty_string(self):
        ticket = ProductFactory.create(product_class=self.tickets,
                          name='blank ticket', upc=None)
        self.assertEqual(ticket.upc, u'')


    def test_upc_uniqueness_enforced(self):
	ticket = ProductFactory.create(product_class=self.tickets,
				      name='blank ticket', upc='a_laker_ticket_to_greatness')

        self.assertRaises(IntegrityError, ProductFactory.create,product_class=self.tickets,
				      name='blank ticket', upc='a_laker_ticket_to_greatness')

    def test_allow_two_products_without_upc(self):
        for x in range(2):
	    ticket = ProductFactory.build(product_class=self.tickets,
				  name='blank ticket', upc=None)

class ProductAttributeCreationTests(TestCase):
    def test_validating_option_attribute(self):
        option_group = AttributeOptionGroupFactory.create()
        option_1 = AttributeOptionFactory.create(group=option_group)
        option_2 = AttributeOptionFactory.create(group=option_group)
        pa = ProductAttributeFactory.create( type='option', option_group=option_group)

        self.assertRaises(ValidationError, pa.validate_value, 'invalid')
        pa.validate_value(option_1)
        pa.validate_value(option_2)

        invalid_option = AttributeOption(option='invalid option')
        self.assertRaises(
            ValidationError, pa.validate_value, invalid_option)

    def test_entity_attributes(self):
	unrelated_object = ProProfileFactory.create()
        attribute = ProductAttributeFactory.create(type='entity')

        attribute_value = ProductAttributeValueFactory.create(
            attribute=attribute, value_entity=unrelated_object)

        self.assertEqual(attribute_value.value, unrelated_object)

