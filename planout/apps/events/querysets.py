from django.db import models
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManagerMixin

import logging
logger = logging.getLogger('werkzeug')

#==================================================================================================
class EventQuerySet(QuerySet):
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
        start = datetime(dt.year, dt.month, dt.day)
        end = start.replace(hour=23, minute=59, second=59)
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
