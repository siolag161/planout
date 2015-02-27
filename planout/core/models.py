# Import the basic Django ORM models library
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.db.models.fields import FieldDoesNotExist
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django.utils.encoding import python_2_unicode_compatible, smart_text
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import GEOSGeometry

from .querysets import PassThroughLocationManager, LocationQuerySet

from model_utils.managers import QueryManager
from .fields import AutoCreatedField, AutoLastModifiedField

from core.fields import AutoSlugField
"""
Trying to get the user model
"""
user_model_label = getattr(settings, "AUTH_USER_MODEL", "auth.User")

class ScoredModel(models.Model):
    """
    Index this one
    """
    score = models.FloatField(default=0.0)
    class Meta:
	abstract = True

#===============================================================================
class PostedModel(models.Model): 
    """ 
    """
    poster = models.ForeignKey(user_model_label, verbose_name=_("Poster"),
			       related_name="posted_%(class)ss", editable=False,)
    class Meta:
	abstract = True
	
#===============================================================================x    
class SluggedModel(models.Model):
    """
    An abstract class for class with a slug
    """
    slug = AutoSlugField(_('Slug'), blank=True, null=True, unique = True, editable=False,)

    def get_url_kwargs(self, **kwargs):
	kwargs.update(getattr(self,'url_kwargsw', {'pk': self.pk, 'slug': self.slug}))
	return kwargs

    @property
    def url_name(self):
	raise NotImplementedError("Implement source from please")

    @property
    def source_from(self):
	if hasattr(self, 'name'):
	    return "name"
	else:
	    raise NotImplementedError("Implement source from please")

	
    def get_absolute_url(self):
	from django.core.urlresolvers import reverse
        return reverse(self.url_name, kwargs=self.get_url_kwargs)
	
    class Meta:
	abstract = True
	
#===============================================================================	
class TimeStampedModel(models.Model):
    created = AutoCreatedField(_('created'), editable=False,)
    modified = AutoLastModifiedField(_('modified'), editable=False,)

    class Meta:
        abstract = True
	
#===============================================================================
class GenericRelatedModel(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
	
#===============================================================================
class TimeFramedModel(models.Model):
    start_time = models.DateTimeField(_('start'), null=True, blank=True)
    end_time = models.DateTimeField(_('end'), null=True, blank=True)

    class Meta:
        abstract = True

	
### base class for all the stuff
#===============================================================================
#@todo: ad translation
@python_2_unicode_compatible
class BaseType(TimeStampedModel, SluggedModel):

    name = models.CharField(max_length=80, help_text=_("Please enter the name"), verbose_name=_("name"))

    # alternative_name = models.CharField(max_length=80,
    # 					help_text=_("Please enter the alternative name"),
    # 					verbose_name=_("alternative name"), blank=True, null=True)
    description = models.TextField(help_text=_("Please enter the description"),
					verbose_name=_("description"), blank=True, null=True)
    url = models.URLField(verbose_name=_("website"), blank=True, null=True)    


    def __str__(self):
	return self.name
    
    @property
    def source_from(self):
	return "name"
    
    class Meta:
        abstract = True

		   
def _field_exists(model_class, field_name):
    return field_name in [f.attname for f in model_class._meta.local_fields]

#===========================================================================================
### base class for all the stuff
@python_2_unicode_compatible
class Location(TimeStampedModel, SluggedModel):

    name = models.CharField(null=True, max_length=80, help_text=_("Please enter the name"), verbose_name=_("name"))
    url = models.URLField(verbose_name=_("website"), blank=True, null=True)

    
    # website = models.URLField(null=True, blank=True,
    # 			      help_text="The authoritative website for this Place, such as a business' homepage.")
    vicinity = models.CharField(max_length=255, help_text='The human-readable address of this place - composed of one or more address components.')  
    #rating = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=2, help_text="Place's rating, from 1.0 to 5.0, based on user reviews.")
    #gmap_url = models.URLField(null=True, blank=True, help_text='The official Google Place Page URL of this establishment.')
    icon_url = models.URLField(null=True, blank=True,)
    coordinates = gismodels.PointField( u"longitude/latitude",
					geography=False, blank=True )
    place_id = models.CharField(max_length=100, null=True, unique=True, help_text="Unique stable identifier denoting this place.")
    
    # objects = gismodels.GeoManager()
    objects = PassThroughLocationManager.for_queryset_class(LocationQuerySet)()

    def set_coords(self,lat,lon):
	self.coordinates = GEOSGeometry('POINT(%s %s)' %(lat,lon))
    
    @property
    def address(self):
	if self.vicinity:
	    return self.vicinity
	else:
	    return self.name
	
    
    def __str__(self):
	return self.name
    
    @property
    def source_from(self):
	return "name"
    # def __str__(self):
    # 	return self.name
    
    # class Meta:
    #     abstract = True
