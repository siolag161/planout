import os.path

from django.test import TestCase, modify_settings
from django.core.urlresolvers import reverse

from events.models import Organization, BasicUser
from .factories import OrganizationFactory, UserFactory

from accounts.models import AvatarField
from avatar.util import (get_avatar_url_or_defaul_url, get_primary_avatar)
from avatar.conf import AvatarConf as config
from django.conf import settings
from django.contrib.auth import get_user_model 

import settings as local_settings

from ..util import (get_login_redirect_url)
from ..test_core.behaviors import  OwnedModelTests,SluggedModelTests,TimeStampedModelTests

import logging
logger = logging.getLogger('werkzeug')
 
#####################################################

def get_or_create(**kwargs):
    try:
	orga = Organization.objects.get(**kwargs)
	created = False
    except Organization.DoesNotExist:
	orga = OrganizationFactory.create(**kwargs)
	created = True
    return orga, created

def objects_size():
    return Organization.objects.count()

#########################################################################

class TestOrganization(OwnedModelTests,SluggedModelTests,TimeStampedModelTests,TestCase):
    model = Organization
    def create_instance(self, **kwargs):
	return OrganizationFactory.create(**kwargs)
	
    def create_new_user(self, **kwargs):
	return UserFactory.create()

class TestOrganizationCRUD(TestOrganization):   
    
    def setUp(self):
	self.user = UserFactory.create(username="bunbun")
	self.organization = OrganizationFactory.create(owner=self.user)

    
    def test_create_new(self):	
	organization2,created = get_or_create(name="orga-2", owner=self.user)
	self.assertEqual(created, True)
	self.assertEqual(objects_size(), 2)
	
    def test_create_and_get(self):
	self.assertEqual(objects_size(), 1)
	organization2,created = get_or_create(name="orga-2", owner=self.user)
	self.assertEqual(created, True)
	self.assertEqual(objects_size(), 2)
	user2 = UserFactory.create(email="alibaba@cuncon.com")
	organization2,created = get_or_create(name="orga-2", owner=self.user)
	self.assertEqual(created, False)
	self.assertEqual(objects_size(), 2)

    def test_checkOwner(self):
	self.assertEqual(self.organization.owner.pk, self.user.pk)
	self.assertEqual(self.user.owned_organizations.count(), 1)
	# creates another organization & assign to user
	organization = get_or_create(name="orga-2", owner=self.user)
	self.assertEqual(self.user.owned_organizations.count(), 2)
