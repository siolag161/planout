from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver

import dateutil.rrule as rrule
from django.utils.encoding import python_2_unicode_compatible

from core.fields import Choices
from django.contrib.gis.db import models as gismodels

from accounts.models import BasicUser, ProfessionalProfile
from tinymce.models import HTMLField

from core.fields import BaseImageField
import core.models as core_models
from core.loading import get_model

from .conf import settings as config
from .fields import AgeRangeField
from .querysets import (PassThroughOccurrenceManager, OccurrenceQuerySet,
			PassThroughEventManager, EventQuerySet)

user_model_label = getattr(settings, "AUTH_USER_MODEL", "auth.User")

#=========================================================================

@python_2_unicode_compatible
class EventProduct(models.Model):
    """
    Joining model between products and events. Exists to allow customising.
    """
    product = models.ForeignKey('products.Product', verbose_name=_("Product"))
    event = models.ForeignKey('events.Event',
                                 verbose_name=_("Event"))
    class Meta:
        #abstract = True
        app_label = 'products'
        ordering = ['product', 'event']
        unique_together = ('event','product') 
        verbose_name = _('Product Event')
        verbose_name_plural = _('Product Events')

    def __str__(self):
        return u"<eventproduct for event '%s'>" % self.event
	
#===============================================================================    
class Event(core_models.PostedModel, core_models.TimeFramedModel, core_models.BaseType):
    # '''
    # Event itself
    # '''
    #======
    EVENT_STATUS = Choices(('cancelled', _('cancelled')), ('postponed', _('postponed')),
    			   ('rescheduled', _('rescheduled')), ('scheduled', _('scheduled')), )
    #======
    # EVENT_CATEGORY = Choices(('performance', _('concert or performance')), ('conference', _('conference')),
    # 			     ('gala', _('diner or gala')), ('competition', _('game or competition')), )
    # #======
    # EVENT_TOPIC = Choices(('business', _('business and professional')), ('charity', _('charity and cause')),
    # 			   ('culture', _('community and culture')), ('family', _('family and education')), )
    #======
    status = models.CharField(choices=EVENT_STATUS,
			      default=EVENT_STATUS.scheduled, max_length=20, verbose_name=_("Event Status"))
    #======
    organizer = models.ForeignKey(ProfessionalProfile, verbose_name=_("Organizer"),
				  related_name="organized_%(class)ss") 

    # poster = 

    # topic =  models.CharField( choices=EVENT_TOPIC, max_length=20,
    # 			       verbose_name=_("Event Topic"), null=True, blank=True,)
    # #======
    # category = models.CharField( choices=EVENT_CATEGORY, max_length=20,
    # 				    verbose_name=_("Event Category"), null=True, blank=True, )


    products = models.ManyToManyField(
    	'products.Product', through=EventProduct,
        verbose_name=_("Products"))
    
    logo =  BaseImageField(blank=True, max_length=1024) #AvatarField(max_length=1024, blank=True)
    
    #============================================
    #age_range = AgeRangeField(blank=True, null=True) #models.CharField(max_length=6, verbose_name=_("Event age range"))
    
    location = models.ForeignKey(core_models.Location, related_name = "events", null=True )
    avenue_name = models.CharField( max_length=40, verbose_name=_("Avenue's name"))
    is_online = models.BooleanField(default=False, verbose_name=_("It's an online event"),)

    @property
    def url_name(self):
	return "event:detail"    
	
    @property
    def source_from(self):
    	return "name"

    # use pass throught for chaining the filtering
    #objects = #PassThroughEventManager.for_queryset_class(EventQuerySet)()


    #---------------------------------------------------------------------------
    
    def add_ticket_type(self, title, quantity, price = 0.0, **kwargs):
	'''
        Add one ticket type the event 
	'''
	Ticket = get_model("tickets", "Ticket")
	ticket_type = Ticket.objects.add_ticket_type(self, title, quantity, price, **kwargs)
	return ticket_type
    
    #---------------------------------------------------------------------------
    def add_occurrences(self, start_time, end_time, **rrule_params):
        '''
        Add one or more occurences to the event using a comparable API to 
        ``dateutil.rrule``. 
        
        If ``rrule_params`` does not contain a ``freq``, one will be defaulted
        to ``rrule.DAILY``.
        
        Because ``rrule.rrule`` returns an iterator that can essentially be
        unbounded, we need to slightly alter the expected behavior here in order
        to enforce a finite number of occurrence creation.
        
        If both ``count`` and ``until`` entries are missing from ``rrule_params``,
        only a single ``Occurrence`` instance will be created using the exact
        ``start_time`` and ``end_time`` values.
        '''
        count = rrule_params.get('count')
        until = rrule_params.get('until')
        if count == until == None:
            self.occurrences.create(start_time=start_time, end_time=end_time)
        else:
            rrule_params.setdefault('freq', rrule.DAILY)
            delta = end_time - start_time
            for ev in rrule.rrule(dtstart=start_time, **rrule_params):
		occ_end_time = ev + delta

                self.occurrences.create(start_time=ev, end_time = occ_end_time)
		if not self.end_time or self.end_time < occ_end_time:
		    self.end_time = occ_end_time

    #---------------------------------------------------------------------------
    def upcoming_occurrences(self):
	from django.utils import timezone
        '''
        Return all occurrences that are set to start on or after the current
        time.
        '''
        return self.occurrences.filter(start_time__gte=timezone.now())

    #---------------------------------------------------------------------------
    def next_occurrence(self):
        '''
        Return the single occurrence set to start on or after the current time
        if available, otherwise ``None``.
        '''
        upcoming = self.upcoming_occurrences()
        return upcoming[0] if upcoming else None

    #---------------------------------------------------------------------------
    def daily_occurrences(self, dt=None):
        '''
        Convenience method wrapping ``Occurrence.objects.daily_occurrences``.
        '''
        return Occurrence.objects.daily_occurrences(dt=dt, event=self)
    
#===============================================================================
class Occurrence(core_models.TimeFramedModel, models.Model):
    '''
    Represents the start end time for a specific occurrence of a master ``Event``
    object.
    '''
    event = models.ForeignKey(Event, verbose_name=_('event'), editable=False, related_name='occurrences')


    objects = PassThroughOccurrenceManager.for_queryset_class(OccurrenceQuerySet)()
    #===========================================================================
    class Meta:
        verbose_name = _('occurrence')
        verbose_name_plural = _('occurrences')
        ordering = ('start_time', 'end_time')

    #---------------------------------------------------------------------------
    def __str__(self):
        return '{}: {}'.format(self.title, self.start_time.isoformat())

    #---------------------------------------------------------------------------
    def __lt__(self, other):
        return self.start_time < other.start_time

    #---------------------------------------------------------------------------
    @property
    def title(self):
        return self.event.title
	
#===============================================================================
# a set of convenience functions
def create_event_with_organization(
	
):
    '''
    Convenience function to create an ``Event``, optionally create an 
    ``EventType``, and associated ``Organization``s.
    '''
    pass

#######################################################
@receiver(pre_save, sender=Event)
def event_pre_save_populate_callback(sender, instance, *args, **kwargs):
    from django.utils import timezone
    '''
    populate ``Event`` instance with default value
    
    '''
    if not instance.start_time:
	instance.start_time = timezone.now()
    if not instance.end_time:
	instance.end_time = instance.start_time + config.EVENT_DEFAULT_OCCURRENCE_DURATION
    
@receiver(pre_save, sender=Occurrence)
def occurrence_pre_save_populate_callback(sender, instance, *args, **kwargs):
    pass
    #logger.warning("OCCURENCE-PRESAVE: please implement whenever remove occurence, modify occurence...")

