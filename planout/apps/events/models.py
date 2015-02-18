from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
import core.models as core_models
from core.fields import Choices
from djgeojson.fields import PointField

from accounts.models import BasicUser
#from avatar.fields import AvatarField

from .fields import AgeRangeField
from core.fields import BaseImageField

# user_model_label = getattr(settings, "AUTH_USER_MODEL", "auth.User")

#class Location(object):
    #pass

class Organization(core_models.OwnedModel, core_models.BaseType):
    '''
    The organizer of the event
    '''    
    # email = models.EmailField(_('email address'), unique=True, max_length=100, blank=True)
    #location = Location # models.CharField(_('address'), max_length=100, blank=True)
    logo =  BaseImageField(blank=True, max_length=1024) #AvatarField(max_length=1024, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    
    '''
    def upcoming_events():
      pass
    def pass_events():
      pass
    '''

    

    @property
    def url_name(self):
	return "organization:detail"

    @property
    def source_from(self):
	return "name"
    
    def __unicode__(self):
	return self.name
#===============================================================================    

#===============================================================================    
class Event(core_models.TimeFramedModel, core_models.BaseType):
    '''
    Event itself
    '''
    #======
    EVENT_STATUS = Choices(('cancelled', _('cancelled')), ('postponed', _('postponed')),
			   ('rescheduled', _('rescheduled')), ('scheduled', _('scheduled')), )
    #======
    EVENT_CATEGORY = Choices(('performance', _('concert or performance')), ('conference', _('conference')),
			     ('gala', _('diner or gala')), ('competition', _('game or competition')), )
    #======
    EVENT_TOPIC = Choices(('business', _('business and professional')), ('charity', _('charity and cause')),
			   ('culture', _('community and culture')), ('family', _('family and education')), )
    #======
    status = models.CharField(choices=EVENT_STATUS,
			      default=EVENT_STATUS.scheduled, max_length=20, verbose_name=_("Event Status"))
    #======
    organizer = models.ForeignKey(Organization, verbose_name=_("Organizer"),
				  related_name="organized_%(class)ss")

    topic =  models.CharField( choices=EVENT_TOPIC, max_length=20,
			       verbose_name=_("Event Topic"), null=True, blank=True,)
    #======
    category = models.CharField( choices=EVENT_CATEGORY, max_length=20,
				    verbose_name=_("Event Category"), null=True, blank=True, )

    logo =  BaseImageField(blank=True, max_length=1024) #AvatarField(max_length=1024, blank=True)
    
    #======
    age_range = AgeRangeField() #models.CharField(max_length=6, verbose_name=_("Event age range"))
    
    # start_time = models.DateTimeField(_('start time'))
    # end_time = models.DateTimeField(_('end time'))
    location = PointField()

    is_online = models.BooleanField(default=False, verbose_name=_("It's an online event"),)

    @property
    def url_name(self):
	return "event:detail"
	
    @property
    def source_from(self):
    	return "name"
    
#===============================================================================
class Occurrence(core_models.TimeFramedModel, models.Model):
    '''
    Represents the start end time for a specific occurrence of a master ``Event``
    object.
    '''
    event = models.ForeignKey(Event, verbose_name=_('event'), editable=False)

    # start_time = models.DateTimeField(_('start time'))
    # end_time = models.DateTimeField(_('end time'))
    # location = Location
    # notes = GenericRelation(Note, verbose_name=_('notes'))
    # objects = OccurrenceManager()
