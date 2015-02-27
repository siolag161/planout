from django.db import models
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManagerMixin


#==================================================================================================
class ProductQuerySet(QuerySet):
    pass
    # def base_queryset(self):
    #     """
    #     Applies select_related and prefetch_related for commonly related
    #     models to save on queries
    #     """
    #     return self.select_related('product_class')\
    #         .prefetch_related('children',
    #                           'product_options',
    #                           'product_class__options',
    #                           'stockrecords',
    #                           'images',
    #                           )

class ProductManager(models.Manager):
    pass

class PassThroughProductManager(PassThroughManagerMixin, ProductManager):
    pass
