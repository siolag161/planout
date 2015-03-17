import os.path

from django.test import TestCase, modify_settings
from django.core.urlresolvers import reverse
 
# from accounts.models import 
from django.conf import settings
from django.contrib.auth import get_user_model 
from django.db import IntegrityError

import logging
logger = logging.getLogger('werkzeug')

from django.db import models

import factory
from tests.factories import UserFactory

# from .models import DummyModel


    
# class ImageFactory(factory.DjangoModelFactory):
#     FACTORY_FOR = DummyModel

class TestImagesUtils(TestCase):
    pass
    # def create_instance(self, **kwargs):
    # 	return ImageFactory.build()
    
    # def setUp(self):
    # 	self.obj = self.create_instance()
	
    # def test_avatar_path(self):
    # 	obj = self.obj
	
    # 	self.assertEqual(obj, "cavangvang")

	
    # def test_image_url(self):
    # 	obj = self.create_instance()
