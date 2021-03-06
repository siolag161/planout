from decimal import Decimal as D
from core.loading import get_model

from django.test import TestCase

from tests import factories

Partner = get_model('accounts', 'ProfessionalProfile')
#PartnerAddress = get_model('partner', 'PartnerAddress')
#Country = get_model('address', 'Country')


class TestStockRecord(TestCase):

    def setUp(self):
        self.product = factories.ProductFactory.create()
        self.stockrecord = factories.StockRecordFactory.create(
	    price_excl_tax=D('10.00'), num_in_stock=10
	)

    def test_get_price_excl_tax_returns_correct_value(self):
        self.assertEqual(D('10.00'), self.stockrecord.price_excl_tax)

    def test_net_stock_level_with_no_allocation(self):
        self.assertEqual(10, self.stockrecord.net_stock_level)

    def test_net_stock_level_with_allocation(self):
        self.stockrecord.allocate(5)
        self.assertEqual(10-5, self.stockrecord.net_stock_level)

    def test_allocated_does_not_alter_num_in_stock(self):
        self.stockrecord.allocate(5)
        self.assertEqual(10, self.stockrecord.num_in_stock)
        self.assertEqual(5, self.stockrecord.num_allocated)

    def test_allocation_handles_null_value(self):
        self.stockrecord.num_allocated = None
        self.stockrecord.allocate(5)

    def test_consuming_allocation(self):
        self.stockrecord.allocate(5)
        self.stockrecord.consume_allocation(3)
        self.assertEqual(2, self.stockrecord.num_allocated)
        self.assertEqual(7, self.stockrecord.num_in_stock)

    def test_cancelling_allocation(self):
        self.stockrecord.allocate(5)
        self.stockrecord.cancel_allocation(4)
        self.assertEqual(1, self.stockrecord.num_allocated)
        self.assertEqual(10, self.stockrecord.num_in_stock)

    def test_cancelling_allocation_ignores_too_big_allocations(self):
        self.stockrecord.allocate(5)
        self.stockrecord.cancel_allocation(6)
        self.assertEqual(0, self.stockrecord.num_allocated)
        self.assertEqual(10, self.stockrecord.num_in_stock)
