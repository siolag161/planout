class TaxNotKnown(Exception):
    """
    Exception for when a tax-inclusive price is requested but we don't know
    what the tax applicable is (yet).
    """


class Price(object):
    """
    Simple price class that encapsulates a price and its tax information
    Attributes:
        incl_tax (Decimal): Price including taxes
        excl_tax (Decimal): Price excluding taxes
        tax (Decimal): Tax amount
        is_tax_known (bool): Whether tax is known
        currency (str): 3 character currency code
    """

    def __init__(self, currency, excl_tax, incl_tax=None, tax=None):
        self.currency = currency
        self.excl_tax = excl_tax
        if incl_tax is not None:
            self.incl_tax = incl_tax
            self.is_tax_known = True
        elif tax is not None:
            self.incl_tax = excl_tax + tax
            self.is_tax_known = True
        else:
            self.incl_tax = None
            self.is_tax_known = False

    def _get_tax(self):
        return self.incl_tax - self.excl_tax

    def _set_tax(self, value):
        self.incl_tax = self.excl_tax + value
        self.is_tax_known = True

    tax = property(_get_tax, _set_tax)

    def __repr__(self):
        if self.is_tax_known:
            return "%s(currency=%r, excl_tax=%r, incl_tax=%r, tax=%r)" % (
                self.__class__.__name__, self.currency, self.excl_tax,
                self.incl_tax, self.tax)
        return "%s(currency=%r, excl_tax=%r)" % (
            self.__class__.__name__, self.currency, self.excl_tax)

    def __eq__(self, other):
        """
        Two price objects are equal if currency, price.excl_tax and tax match.
        """
        return (self.currency == other.currency and
                self.excl_tax == other.excl_tax and
                self.incl_tax == other.incl_tax)



class Base(object):
    """
    The interface that any pricing policy must support
    """

    #: Whether any prices exist
    exists = False

    #: Whether tax is known
    is_tax_known = False

    #: Price excluding tax
    excl_tax = None

    #: Price including tax
    incl_tax = None

    #: Price to use for offer calculations
    @property
    def effective_price(self):
        # Default to using the price excluding tax for calculations
        return self.excl_tax

    #: Price tax
    tax = None

    #: Retail price
    retail = None

    #: Price currency (3 char code)
    currency = None

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.__dict__)


class Unavailable(Base):
    """
    This should be used as a pricing policy when a product is unavailable and
    no prices are known.
    """


class FixedPrice(Base):
    """
    This should be used for when the price of a product is known in advance.
    It can work for when tax isn't known (like in the US).
    Note that this price class uses the tax-exclusive price for offers, even if
    the tax is known.  This may not be what you want.  Use the
    TaxInclusiveFixedPrice class if you want offers to use tax-inclusive
    prices.
    """
    exists = True

    def __init__(self, currency, excl_tax, tax=None):
        self.currency = currency
        self.excl_tax = excl_tax
        self.tax = tax

    @property
    def incl_tax(self):
        if self.is_tax_known:
            return self.excl_tax + self.tax
        raise TaxNotKnown(
            "Can't calculate price.incl_tax as tax isn't known")

    @property
    def is_tax_known(self):
        return self.tax is not None


class TaxInclusiveFixedPrice(FixedPrice):
    """
    Specialised version of FixedPrice that must have tax passed.  It also
    specifies that offers should use the tax-inclusive price (which is the norm
    in the UK).
    """
    exists = is_tax_known = True

    def __init__(self, currency, excl_tax, tax):
        self.currency = currency
        self.excl_tax = excl_tax
        self.tax = tax

    @property
    def incl_tax(self):
        return self.excl_tax + self.tax

    @property
    def effective_price(self):
        return self.incl_tax
