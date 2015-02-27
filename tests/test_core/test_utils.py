import os.path

from django.test import TestCase, modify_settings
from django.core.urlresolvers import reverse
 
# from accounts.models import 
from avatar.util import (get_avatar_url_or_defaul_url, get_primary_avatar)
from avatar.conf import AvatarConf as config
from django.conf import settings
from django.contrib.auth import get_user_model 
from django.db import IntegrityError


import logging
logger = logging.getLogger('werkzeug')

from tests.factories import UserFactory

#class ImageConfig(

