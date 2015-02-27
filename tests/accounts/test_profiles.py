from django.db import DataError
from .factories import *

import os.path

from django.test import TestCase, modify_settings
from django.core.urlresolvers import reverse

from tests.factories import *

from avatar.util import (get_avatar_url_or_defaul_url, get_primary_avatar)
from avatar.conf import settings as config
from django.conf import settings
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.validators import to_python

from ..util import (get_login_redirect_url)

import json

import logging
logger = logging.getLogger('werkzeug')
 
#####################################################
def upload_helper(o, filename):
    f = open(os.path.join(o.testdatapath, filename), "rb")
    response = o.client.post(reverse('avatar:avatar_add'), {
        'avatar': f,
	'avatar_data': json.dumps({"x":154.39999999999998,"y":43.899999999999984,
				   "height":351.20000000000005,"width":351.20000000000005})
    }, follow=True)
    f.close()
    return response

@modify_settings(
    
)

class NonAuthenticatedProProfileTestCase(TestCase):
    def setUp(self):
	self.testdatapath = os.path.join(os.path.dirname(__file__), "data")
	self.username = 'testuser'
	self.password = 'testpass'
	self.email = 'bunbun@gmail.com'
	
	User = get_user_model()
	self.user = User.objects.create_user( email=self.email, password=self.password)
	logged_in = self.client.login(username = self.username, email = self.email, password = "")
	self.assertFalse(logged_in)
    	self.profile = ProProfileFactory.create(owner = self.user, name = "Pro Bono")

    
class AuthenticatedProProfileTestCase(TestCase):
    def setUp(self):
	self.testdatapath = os.path.join(os.path.dirname(__file__), "data")
	self.username = 'testuser'
	self.password = 'testpass'
	self.email = 'bunbun@gmail.com'
	
	User = get_user_model()
	self.user = User.objects.create_user( email=self.email, password=self.password)
	logged_in = self.client.login(username = self.username, email = self.email, password = "")
	self.assertFalse(logged_in)

	self.profile = ProProfileFactory.create(owner = self.user, name = "Pro Bono")
   
#==============================================================
class AuthenticatedProProfile(AuthenticatedProProfileTestCase):
    def test_creation(self):
	self.assertEqual(self.user.pro_profiles.count(), 1)

    def test_phone(self):
	pass

