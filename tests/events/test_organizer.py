import os.path

from django.test import TestCase, modify_settings
from django.core.urlresolvers import reverse

from events.models import ProfessionalProfile, BasicUser
from tests.factories import ProProfileFactory, UserFactory

from accounts.models import AvatarField
from avatar.util import (get_avatar_url_or_defaul_url, get_primary_avatar)
from avatar.conf import AvatarConf as config
from django.conf import settings
from django.contrib.auth import get_user_model 

import settings as local_settings

from ..util import (get_login_redirect_url)
from ..test_core.behaviors import SluggedModelTests,TimeStampedModelTests,PostedModelTests

import logging
logger = logging.getLogger('werkzeug')
 
#####################################################

def get_or_create(**kwargs):
    try:
	orga = ProfessionalProfile.objects.get(**kwargs)
	created = False
    except ProfessionalProfile.DoesNotExist:
	orga = ProProfileFactory.create(**kwargs)
	created = True
    return orga, created

def objects_size():
    return ProfessionalProfile.objects.count()

#########################################################################

class TestProfessionalProfile(SluggedModelTests,TimeStampedModelTests,TestCase):
    model = ProfessionalProfile
    def create_instance(self, **kwargs):
	return ProProfileFactory.create(**kwargs)
	
    def create_new_user(self, **kwargs):
	return UserFactory.create()

class TestProfessionalProfileCRUD(TestProfessionalProfile):   
    
    def setUp(self):
	self.user = UserFactory.create(username="bunbun")
	self.proprofile = ProProfileFactory.create(owner=self.user)

    
    def test_create_new(self):	
	proprofile2,created = get_or_create(name="orga-2", owner=self.user)
	self.assertEqual(created, True)
	self.assertEqual(objects_size(), 2)
	
    def test_create_and_get(self):
	self.assertEqual(objects_size(), 1)
	proprofile2,created = get_or_create(name="orga-2", owner=self.user)
	self.assertEqual(created, True)
	self.assertEqual(objects_size(), 2)
	user2 = UserFactory.create(email="alibaba@cuncon.com")
	proprofile2,created = get_or_create(name="orga-2", owner=self.user)
	self.assertEqual(created, False)
	self.assertEqual(objects_size(), 2)

    def test_checkOwner(self):
	self.assertEqual(self.proprofile.owner.pk, self.user.pk)
	self.assertEqual(self.user.pro_profiles.count(), 1)
	# creates another proprofile & assign to user
	proprofile = get_or_create(name="orga-2", owner=self.user)
	self.assertEqual(self.user.pro_profiles.count(), 2)

