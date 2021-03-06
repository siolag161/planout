from django.db import models
from django.contrib.gis.db import models as gis_models
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManagerMixin

from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.gis.db.models.query import GeoQuerySet


from prices import Price

import logging
logger = logging.getLogger('werkzeug')

#==================================================================================================


class TimeFramedQuerySet(QuerySet):
    '''
    '''
    def from_datetime(self, from_dt = None):
	if not from_dt:
	    ''' we offset back 1 hour  '''
	    from_dt = timezone.now() - timedelta(hours = 1)
	qs = self.filter( 
            models.Q(
                start_time__gte = from_dt,
            )
        )
	return qs
		    
    def until_datetime(self, to_dt = None):
	if not to_dt:
	    to_dt = timezone.now().replace(hour=23, minute=59, second=59, microsecond=99999)	
	qs = self.filter( 
            models.Q(
                start_time__lte = to_dt,
            )
        )
	return qs
    
    '''
    '''
    def datetimeframe(self, from_dt = None, to_dt = None):
	return self.from_datetime(from_dt).until_datetime(to_dt)

    ################################################
    def dayframe(self, from_dt = None, to_dt = None):
	right_now = timezone.now()
	if not from_dt:
	    ''' we offset back 2 hours  '''
	    from_dt = right_now

	if ( from_dt -right_now ).days >= 1:
	    ''' if not today then we should restart the date to midnight '''
	    from_dt = from_dt.replace(hour=0, minute=0, second=0, microsecond=0)
	else:
	    ''' we offset back 1 hours  '''
	    from_dt = max( from_dt.replace(hour=0, minute=0, second=0, microsecond=0),
			   from_dt - timedelta(hours = 1 ))
	    
	if not to_dt:
	    to_dt = from_dt.replace(hour=23, minute=59, second=59, microsecond=99999)

	return self.datetimeframe(from_dt, to_dt)
	
    def by_day(self, dt):
    	'''
        Returns a queryset of for instances that occurs during a day (strictly within this day,
    	not just overlapping)
        
        * ``dt`` may be either a datetime.datetime, datetime.date object, or
          ``None``. If ``None``, default to the current day.        
        '''
	dt = dt or timezone.now()	
	dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    	return self.dayframe(dt)

    def today(self):
	''' convenience method '''
	from_dt = timezone.now()
	return self.by_day(from_dt)

    def tomorrow(self):
	dt = timezone.now() + timedelta(days=1)
	return self.by_day(dt)

    '''    
    '''
    def this_month(self):
    	from_dt = timezone.now() 
    	# mid-night last_day of the month
    	last_day = from_dt + relativedelta( day=1, months=+1, days=-1)

    	return self.dayframe(from_dt, last_day)
	

    def this_week(self):
    	from_dt = timezone.now()
    	last_week_day = from_dt + timedelta(days=7-from_dt.weekday()-1)
    	return self.dayframe(from_dt, last_week_day)

    def next_week(self):
	today = timezone.now()
    	from_dt = today + timedelta(days=-today.weekday(), weeks=1)
    	last_week_day = from_dt + timedelta(days=6)
    	return self.dayframe(from_dt, last_week_day)

    # #################################
    # def next_n_days(self):
    # 	pass
	
#==================================================================================================

class EventGeoQuerySet(GeoQuerySet):
    def within_bound(self, bound_geom):
	qs = self.filter(location__coordinates__within=bound_geom)
	return qs

    def within_bbox(self, bbox):
	from django.contrib.gis.geos import Polygon
	bound_geom = Polygon.from_bbox(bbox)
	
	return self.within_bound(bound_geom)
	
class EventQuerySet(TimeFramedQuerySet, EventGeoQuerySet):
    #### filter by price =======
    """
    todo: remove currency here, find a new currency
    """
    def within_price_range(self, min_val, max_val, currency = None):
	if not currency:
	    currency = settings.DEFAULT_CURRENCY
	min_price = Price(min_val, currency=currency)
	max_price = Price(max_val, currency=currency)
	qs = self.prefetch_related('tickets').filter(tickets__price__range = (min_price, max_price)).distinct()
	return qs

    def is_free(self, currency = None):
	if not currency:
	    currency = settings.DEFAULT_CURRENCY
	return self.within_price_range(0, 0, currency)

    def is_available(self):
	qs = self.prefetch_related().filter(tickets__stock__gt=0).distinct()
	return qs

	raise NotImplementedError("implement event avai please")

###============================
class EventManager(gis_models.GeoManager):
    pass

class PassThroughEventManager(PassThroughManagerMixin, EventManager):
    pass

#==================================================================================================
class OccurrenceManager(models.Manager):
    use_for_related_fields = True

class PassThroughOccurrenceManager(PassThroughManagerMixin, OccurrenceManager):
    pass
    
class OccurrenceQuerySet(QuerySet):
    def daily_occurrences(self, dt=None, event=None):
        '''
        Returns a queryset of for instances that have any overlap with a 
        particular day.
        
        * ``dt`` may be either a datetime.datetime, datetime.date object, or
          ``None``. If ``None``, default to the current day.
        
        * ``event`` can be an ``Event`` instance for further filtering.
        '''
	from django.utils import timezone
	from datetime import datetime
	
	dt = dt or timezone.now()	
        start = dt.replace(hour=0, minute=0, second = 0)
        end = dt.replace(hour=23, minute=59, second=59)
	
	logger.warning("timezone-ware-here (OccManager) please")
        qs = self.filter(
            models.Q(
                start_time__gte=start,
                start_time__lte=end,
            ) |
            models.Q(
                end_time__gte=start,
                end_time__lte=end,
            ) |
            models.Q(
                start_time__lt=start,
                end_time__gt=end
            )
        )

        return qs.filter(event=event) if event else qs
