import django

from core.loading import is_model_registered
from .abstract_models import *

__all__ = ['ProductAttributesContainer']

if not is_model_registered('products', 'ProductClass'):
    class ProductClass(AbstractProductClass):
        pass

    __all__.append('ProductClass')


if not is_model_registered('products', 'Product'):
    class Product(AbstractProduct):
        pass
    __all__.append('Product')



if not is_model_registered('products', 'ProductAttribute'):
    class ProductAttribute(AbstractProductAttribute):
        pass
    __all__.append('ProductAttribute')


if not is_model_registered('products', 'ProductAttributeValue'):
    class ProductAttributeValue(AbstractProductAttributeValue):
        pass
    __all__.append('ProductAttributeValue')


if not is_model_registered('products', 'AttributeOptionGroup'):
    class AttributeOptionGroup(AbstractAttributeOptionGroup):
        pass
    __all__.append('AttributeOptionGroup')


if not is_model_registered('products', 'AttributeOption'):
    class AttributeOption(AbstractAttributeOption):
        pass
    __all__.append('AttributeOption')
