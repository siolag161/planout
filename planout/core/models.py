# Import the basic Django ORM models library
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from .fields import AutoCreatedField, AutoLastModifiedField

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

class OwnedModel(models.Model): 
    """ 
    """
    owner = models.ForeignKey(user_model_label, verbose_name=_("Owner"), related_name="%(class)ss")

    class Meta:
	abstract = True
    
class SluggedModel(models.Model):
    """
    An abstract class for class with a slug
    """
    name = models.CharField(max_length=80, help_text=_("Please enter the name"), verbose_name=_("name"))

    slug = models.SlugField(_('Slug'), null=True)

    #@permalink
    def get_absolute_url(self):
        # return reverse('detail', kwargs= {
        #     'slug': self.slug,
        #     'id': self.id,
        # })
	return "%s-%s" % (self.slug, self.id)
    
    class Meta:
	abstract = True
	
class TimeStampedModel(models.Model):
    created = AutoCreatedField(_('created'))
    modified = AutoLastModifiedField(_('modified'))

    class Meta:
        abstract = True

class TimeFramedModel(models.Model):
    start = models.DateTimeField(_('start'), null=True, blank=True)
    end = models.DateTimeField(_('end'), null=True, blank=True)

    class Meta:
        abstract = True

	
### base class for all the stuff
class BaseType(OwnedModel, TimeStampedModel, SluggedModel):
    alternative_name = models.CharField(max_length=80,
					help_text=_("Please enter the alternative name"),
					verbose_name=_("alternative name"))
    description = models.TextField(help_text=_("Please enter the description"),
					verbose_name=_("desciption"))
    url = models.URLField()
    class Meta:
        abstract = True

				   

