from django.db import DataError
from django.test import TestCase
import os.path
from django.core.urlresolvers import reverse

from django.conf import settings 
from django.contrib.auth import get_user_model 

from ..util import (get_login_redirect_url)

import json

from tests.factories import UserFactory
import accounts.util as utils
 
import logging
logger = logging.getLogger('werkzeug')
#####################################################
def upload_helper(o, filename):
    f = open(os.path.join(o.testdatapath, filename), "rb")
    response = o.client.post(reverse('profiles:avatar_add'), {
        'avatar': f,
	'avatar_data': json.dumps({"x":154.39999999999998,"y":43.899999999999984,
				   "height":351.20000000000005,"width":351.20000000000005})
    }, follow=True)
    f.close()
    return response

#=======================================================================================
class AvatarNonAuthenticatedTestCase(TestCase):
    def setUp(self):
	self.testdatapath = os.path.join(os.path.dirname(__file__), "data")
	self.username = 'testuser'
	self.password = 'testpass'
	self.email = 'bunbun@gmail.com'
	
	User = get_user_model()
	self.user = User.objects.create_user( email=self.email, password=self.password)
	logged_in = self.client.login(username = self.username, email = self.email, password = "")
	self.assertFalse(logged_in)

    def test_login(self):
	self.assertEqual(self.user.email, "bunbun@gmail.com")

    def test_uploadNormal(self):
    	response = upload_helper(self, "default_avatar.jpg")
        self.assertEqual(response.status_code, 200)
	self.assertRedirects(response, get_login_redirect_url(reverse('profiles:avatar_add')) )
	
class AvatarAuthenticatedTestCase(TestCase):
    def setUp(self):
	self.testdatapath = os.path.join(os.path.dirname(__file__), "data")
	self.username = 'testuser'
	self.password = 'testpass'
	self.email = 'bunbun@gmail.com'	
	User = get_user_model()
	self.user = User.objects.create_user( email=self.email, password=self.password)
	logged_in = self.client.login(username = self.username, email = self.email, password = self.password)
	self.assertTrue(logged_in)

    def test_login(self):
	self.assertEqual(self.user.email, "bunbun@gmail.com")
	
    def test_defaultAvatar(self):
    	avatar_url = utils.get_avatar_url_or_defaul_url(self.user)
    	supposed_url = "%s%s" %(getattr(settings, 'MEDIA_URL', None), settings.PROFILE_AVATAR_DEFAULT_URL)
    	self.assertEqual(avatar_url, supposed_url)

    def test_uploadNormal(self):
    	response = upload_helper(self, "default_avatar.jpg")
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.context['upload_avatar_form'].errors, {})
    	# avatar = get_primary_avatar(response.context['user'])
    	# self.user = response.context['user']
	# avatar_url = get_avatar_url_or_defaul_url(self.user)
    	# supposed_url = "%s%s" %(getattr(settings, 'MEDIA_URL', None),  config.AVATAR_DEFAULT_URL)
    	# self.assertNotEqual(avatar_url, supposed_url)
	
#     def test_uploadEmptyFile(self):
#     	response = upload_helper(self, "emptyFile")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.context['upload_avatar_form'].errors,
#     			 {'avatar': [u'The submitted file is empty.']})

#     # def test_uploadNonImageFile(self):
#     # 	response = upload_helper(self, "randomFile")
#     #     self.assertEqual(response.status_code, 200)
#     # 	self.assertNotEqual(response.context['upload_avatar_form'].errors,
#     # 			  {})

#     def test_uploadIncorrectFileType(self):
#     	response = upload_helper(self, "default_avatar")
#         self.assertEqual(response.status_code, 200)
# 	self.assertTrue( 'invalid file extension' in response.context['upload_avatar_form'].errors['avatar'][0])

#     def test_uploadBigFile(self):
#     	response = upload_helper(self, "bigFile.jpg")
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue( 'Your file is too big' in response.context['upload_avatar_form'].errors['avatar'][0])
    
	
	
   

    
    
