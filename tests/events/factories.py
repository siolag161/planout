import factory # factory 

from ..accounts.factories import UserFactory
from events import models
from django.utils import timezone

from datetime import datetime, timedelta

def get_tz_aware(dt):
    if dt.tzinfo is None:
	return timezone.make_aware(dt, timezone.get_default_timezone())
    else:
	return dt

class OrganizationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Organization
    owner = factory.SubFactory(UserFactory)
    name = "an organization"
    url = "http://orga.com"
    email = "bun@orga.com"

    class Meta:
	django_get_or_create = ('name', 'owner',)

class EventFactory(factory.DjangoModelFactory):
    FACTORY_FOR = models.Event
    organizer = factory.SubFactory(OrganizationFactory)
    status = models.Event.EVENT_STATUS.scheduled
    topic = models.Event.EVENT_TOPIC.business
    category = models.Event.EVENT_CATEGORY.performance
    age_range = (0,99)
    start_time = factory.Sequence(lambda n: get_tz_aware(timezone.now() + timedelta(days = n) ))
    end_time = factory.Sequence(lambda n: get_tz_aware(timezone.now() + timedelta(days = n, hours = 2) ))
    location = {'type': 'Point', "coordinates": [
	10.768107,
	106.66577
    ]}

    @classmethod
    def _setup_next_sequence(cls):      
      return getattr(cls, 'starting_seq_num', 0)

    
