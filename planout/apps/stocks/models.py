import django

from core.loading import is_model_registered
from .abstract_models import (  AbstractStockRecord)

__all__ = []




if not is_model_registered('stocks', 'StockRecord'):
    class StockRecord(AbstractStockRecord):
        pass

    __all__.append('StockRecord')

