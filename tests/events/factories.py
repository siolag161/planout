import factory # factory 

from ..accounts.factories import UserFactory
from events import models

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
    location = {'type': 'Point', "coordinates": [
	10.768107,
	106.66577
    ]}

    
