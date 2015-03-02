import os.path

from django.test import TestCase, modify_settings
from django.core.urlresolvers import reverse
 
from django.conf import settings
from django.contrib.auth import get_user_model 
from django.db import IntegrityError

import logging
logger = logging.getLogger('werkzeug')

from tests.factories import LocationFactory, core_models
from django.contrib.gis.geos import Point, Polygon


#========================================
class TestBuild(TestCase):
    def setUp(self):
	self.loc = LocationFactory.build()
	self.assertEqual(self.loc.coordinates.x, 10.750823)
	self.assertEqual(self.loc.coordinates.y, 106.667536)
	
    def test_coord(self):
	self.loc.set_coords(12,34)	
	self.assertEqual(self.loc.coordinates.x, 12)
	self.assertEqual(self.loc.coordinates.y, 34)

class TestCreate(TestCase):
    def setUp(self):
	self.loc = LocationFactory.build()
	self.loc.set_coords(10,10)
	self.loc.save()
	self.assertEqual(self.loc.coordinates.x, 10)
	self.assertEqual(self.loc.coordinates.y, 10)

    def test_filter_bounding(self):	
	bound_rec = Polygon.from_bbox((9,106,11,108))	
	self.pts = LocationFactory.create_batch(10)
	self.assertEqual(core_models.Location.objects.count(), 11)
	filtered_pts = core_models.Location.objects.filter(coordinates__within=bound_rec)
	self.assertEqual(filtered_pts.count(), 10)
	self.loc.set_coords(10,10)

	filtered_pts = core_models.Location.objects.filter(coordinates__within=bound_rec)
	self.assertEqual(filtered_pts.count(), 10)

class TestUpdate(TestCase):
    pass


    
