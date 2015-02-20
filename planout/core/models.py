# Import the basic Django ORM models library
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.db.models.fields import FieldDoesNotExist
from django.core.exceptions import ImproperlyConfigured
from django.utils.timezone import now

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
class OwnedModel(models.Model): 
    """ 
    """
    owner = models.ForeignKey(user_model_label, verbose_name=_("Owner"), related_name="owned_%(class)ss")

    class Meta:
	abstract = True
	
#===============================================================================x    
class SluggedModel(models.Model):
    """
    An abstract class for class with a slug
    """
    slug = AutoSlugField(_('Slug'), blank=True, null=True)

    def get_url_kwargs(self, **kwargs):
	kwargs.update(getattr(self,'url_kwargsw', {'pk': self.pk, 'slug': self.slug}))
	return kwargs

    @property
    def url_name(self):
	raise NotImplementedError("Implement source from please")
	#return "event:detail"
    
    @property
    def source_from(self):
	raise NotImplementedError("Implement source from please")

	
    def get_absolute_url(self):
	from django.core.urlresolvers import reverse
        return reverse(self.url_name, kwargs=self.get_url_kwargs)
	
    class Meta:
	abstract = True
	
#===============================================================================	
class TimeStampedModel(models.Model):
    created = AutoCreatedField(_('created'))
    modified = AutoLastModifiedField(_('modified'))

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
class BaseType(TimeStampedModel, SluggedModel):

    name = models.CharField(max_length=80, help_text=_("Please enter the name"), verbose_name=_("name"))

    # alternative_name = models.CharField(max_length=80,
    # 					help_text=_("Please enter the alternative name"),
    # 					verbose_name=_("alternative name"), blank=True, null=True)
    description = models.TextField(help_text=_("Please enter the description"),
					verbose_name=_("desciption"), blank=True, null=True)
    url = models.URLField(verbose_name=_("website"), blank=True, null=True)    
    
    class Meta:
        abstract = True

				   

### base class for all the stuff
#===============================================================================
#@todo: ad translation
# class ventFactory(factory.DjangoModelFactory):
#     FACTORY_FOR = models.Event
#     username = factory.Sequence(lambda n: 'user' + str(n))
def add_timeframed_query_manager(sender, **kwargs):
    """
    Add a QueryManager for a specific timeframe.
    """
    if not issubclass(sender, TimeFramedModel):
        return
    if _field_exists(sender, 'timeframed'):
        raise ImproperlyConfigured(
            "Model '%s' has a field named 'timeframed' "
            "which conflicts with the TimeFramedModel manager."
            % sender.__name__
        )
    sender.add_to_class('timeframed', QueryManager(
        (models.Q(start_date__lte=now) | models.Q(start_date__isnull=True)) &
        (models.Q(end_date__gte=now) | models.Q(end_date__isnull=True))
    ))


models.signals.class_prepared.connect(add_timeframed_query_manager)

def _field_exists(model_class, field_name):
    return field_name in [f.attname for f in model_class._meta.local_fields]
