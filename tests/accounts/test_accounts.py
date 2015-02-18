import os.path

from django.test import TestCase, modify_settings
from django.core.urlresolvers import reverse

from .factories import *
 
# from accounts.models import 
from avatar.util import (get_avatar_url_or_defaul_url, get_primary_avatar)
from avatar.conf import AvatarConf as config
from django.conf import settings
from django.contrib.auth import get_user_model 
from django.db import IntegrityError
import settings as local_settings
from ..util import (get_login_redirect_url)

import logging
logger = logging.getLogger('werkzeug')
 

def signup_helper(o, filename):
    f = open(os.path.join(o.testdatapath, filename), "rb")
    response = o.client.post(reverse('avatar:avatar_add'), {
        'avatar': f,
    }, follow=True)
    f.close()
    return response
    
class UserAccountCreate(TestCase):
    def setUp(self):
	pass
	# self.settings = local_settings
	# self.testdatapath = os.path.join(os.path.dirname(__file__), "data")
	# self.username = 'testuser'
	# self.password = 'testpass'
	# self.email = 'bunbun@gmail.com'

    def test_UUID(self):
    	user1 = UserFactory.create(email="cavang1@bun.com")
    	user2 = UserFactory.create(email="cavang2@bun.com")
    	self.assertEqual(len(user1.uuid),22)
    	self.assertEqual(len(user2.uuid),22)
    	self.assertNotEqual(user1.uuid,user2.uuid)

    def test_UniqueEmail(self):
	# error raised once duplicate email
    	user1 = UserFactory.create(email="cavang1@bun.com")
    	self.assertRaises(IntegrityError, UserFactory.create, email="cavang1@bun.com")

    def test_userNameFromEmail(self):
	pass
    	# user1 = UserFactory.create(email="cavang@bun.com")
	# self.assertEqual(user1.username, "cavang")
	# user2 = UserFactory.create(email="cavang@bun1.com")
	# self.assertEqual(user2.username, "cavang1")

