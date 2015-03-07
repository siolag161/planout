from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from core import models as core_models

def get_default_currency():
    """
    For use as the default value for currency fields.  Use of this function
    prevents Django's core migration engine from interpreting a change to
    OSCAR_DEFAULT_CURRENCY as something it needs to generate a migration for.
    """
    return settings.DEFAULT_CURRENCY

@python_2_unicode_compatible
class AbstractStockRecord(core_models.TimeStampedModel):
    """
    A stock record.
    This records information about a product from a fulfilment partner, such as
    their SKU, the number they have in stock and price information.
    Stockrecords are used by 'strategies' to determine availability and pricing
    information for the customer.
    """
    product = models.ForeignKey(
        'products.Product', related_name="stockrecords",
        verbose_name=_("Product"))
    partner = models.ForeignKey(
        'accounts.ProfessionalProfile', verbose_name=_("Partner"),
        related_name='stockrecords')

    #: The fulfilment partner will often have their own SKU for a product,
    #: which we store here.  This will sometimes be the same the product's UPC
    #: but not always.  It should be unique per partner.
    #: See also http://en.wikipedia.org/wiki/Stock-keeping_unit
    partner_sku = models.CharField(_("Partner SKU"), max_length=128)

    # Price info:
    price_currency = models.CharField(
        _("Currency"), max_length=12, default=get_default_currency)

    # This is the base price for calculations - tax should be applied by the
    # appropriate method.  We don't store tax here as its calculation is highly
    # domain-specific.  It is NULLable because some items don't have a fixed
    # price but require a runtime calculation (possible from an external
    # service).
    price_excl_tax = models.DecimalField(
        _("Price (excl. tax)"), decimal_places=2, max_digits=12,
        blank=True, null=True)

    #: Retail price for this item.  This is simply the recommended price from
    #: the manufacturer.  If this is used, it is for display purposes only.
    #: This prices is the NOT the price charged to the customer.
    price_retail = models.DecimalField(
        _("Price (retail)"), decimal_places=2, max_digits=12,
        blank=True, null=True)

    #: Cost price is the price charged by the fulfilment partner.  It is not
    #: used (by default) in any price calculations but is often used in
    #: reporting so merchants can report on their profit margin.
    cost_price = models.DecimalField(
        _("Cost Price"), decimal_places=2, max_digits=12,
        blank=True, null=True)

    #: Number of items in stock
    num_in_stock = models.PositiveIntegerField(
        _("Number in stock"), blank=True, null=True)

    #: The amount of stock allocated to orders but not fed back to the master
    #: stock system.  A typical stock update process will set the num_in_stock
    #: variable to a new value and reset num_allocated to zero
    num_allocated = models.IntegerField(
        _("Number allocated"), blank=True, null=True)

    #: Threshold for low-stock alerts.  When stock goes beneath this threshold,
    #: an alert is triggered so warehouse managers can order more.
    low_stock_threshold = models.PositiveIntegerField(
        _("Low Stock Threshold"), blank=True, null=True)

    def __str__(self):
        msg = u"Partner: %s, product: %s" % (
            self.partner.display_name, self.product,)
        if self.partner_sku:
            msg = u"%s (%s)" % (msg, self.partner_sku)
        return msg

    class Meta:
        abstract = True
        app_label = 'stocks'
        unique_together = ('partner', 'partner_sku')
        verbose_name = _("Stock record")
        verbose_name_plural = _("Stock records")

    @property
    def net_stock_level(self):
        """
        The effective number in stock (eg available to buy).
        This is correct property to show the customer, not the num_in_stock
        field as that doesn't account for allocations.  This can be negative in
        some unusual circumstances
        """
        if self.num_in_stock is None:
            return 0
        if self.num_allocated is None:
            return self.num_in_stock
        return self.num_in_stock - self.num_allocated

    # 2-stage stock management model

    def allocate(self, quantity):
        """
        Record a stock allocation.
        This normally happens when a product is bought at checkout.  When the
        product is actually shipped, then we 'consume' the allocation.
        """
        if self.num_allocated is None:
            self.num_allocated = 0
        self.num_allocated += quantity
        self.save()
    allocate.alters_data = True

    def is_allocation_consumption_possible(self, quantity):
        """
        Test if a proposed stock consumption is permitted
        """
        return quantity <= min(self.num_allocated, self.num_in_stock)

    def consume_allocation(self, quantity):
        """
        Consume a previous allocation
        This is used when an item is shipped.  We remove the original
        allocation and adjust the number in stock accordingly
        """
        if not self.is_allocation_consumption_possible(quantity):
            raise InvalidStockAdjustment(
                _('Invalid stock consumption request'))
        self.num_allocated -= quantity
        self.num_in_stock -= quantity
        self.save()
    consume_allocation.alters_data = True

    def cancel_allocation(self, quantity):
        # We ignore requests that request a cancellation of more than the
        # amount already allocated.
        self.num_allocated -= min(self.num_allocated, quantity)
        self.save()
    cancel_allocation.alters_data = True

    @property
    def is_below_threshold(self):
        if self.low_stock_threshold is None:
            return False
        return self.net_stock_level < self.low_stock_threshold
