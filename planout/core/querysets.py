from django.db import models
from django.contrib.gis.db import models as gis_models
from django.db.models.query import QuerySet
from django.contrib.gis.db.models.query import GeoQuerySet

from model_utils.managers import PassThroughManagerMixin, QueryManagerMixin


class LocationQuerySet(GeoQuerySet):
    pass

###============================
class LocationManager(gis_models.GeoManager):
    use_for_related_fields = True

class PassThroughLocationManager(PassThroughManagerMixin, LocationManager):
    pass
