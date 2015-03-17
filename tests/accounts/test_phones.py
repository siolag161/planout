# -*- coding: utf-8 -*-

from django.test.testcases import TestCase
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.validators import to_python

from tests.factories import ProfessionalProfile, ProProfileFactory


# import logging
# logger = logging.getLogger('werkzeug')

class PhoneNumberFieldTestCase(TestCase):
    test_number_1 = '+414204242'
    equal_number_strings = ['+44 113 8921113', '+441138921113']
    local_numbers = [
        ('GB', '01606 751 78'),
        ('DE', '0176/96842671'),
    ]
    invalid_numbers = ['+44 113 892111', ]

    def test_valid_numbers_are_valid(self):
        numbers = [PhoneNumber.from_string(number_string)
                   for number_string in self.equal_number_strings]
        self.assertTrue(all([number.is_valid() for number in numbers]))
        numbers = [PhoneNumber.from_string(number_string, region=region)
                   for region, number_string in self.local_numbers]
        self.assertTrue(all([number.is_valid() for number in numbers]))

    def test_invalid_numbers_are_invalid(self):
        numbers = [PhoneNumber.from_string(number_string)
                   for number_string in self.invalid_numbers]
        self.assertTrue(all([not number.is_valid() for number in numbers]))

    def test_objects_with_same_number_are_equal(self):
	numbers = [
	    ProProfileFactory.create(phone_number = number_string).phone_number
	    for number_string in self.equal_number_strings
	]
	self.assertTrue(all(n == numbers[0] for n in numbers))

    def test_field_returns_correct_type(self):
	profile = ProProfileFactory.create()
        self.assertEqual(profile.phone_number, None)		
        profile.phone_number = '+49 176 96842671'
        self.assertEqual(type(profile.phone_number), PhoneNumber)

    def test_fr_number(self):
	profile = ProProfileFactory.create(phone_number="+330652734709")
        phone_number = PhoneNumber.from_string('+33 652734709')
        self.assertEqual(profile.phone_number, phone_number)
        phone_number = PhoneNumber.from_string('+33 0652734709')
        self.assertEqual(profile.phone_number, phone_number)
	
    def test_can_assign_string_phone_number(self):
	profile = ProProfileFactory.create(phone_number = self.test_number_1)
        self.assertEqual(type(profile.phone_number), PhoneNumber)
        self.assertEqual(profile.phone_number.as_e164, self.test_number_1)

    def test_does_not_fail_on_invalid_values(self):
        # testcase for
        # https://github.com/stefanfoulis/django-phonenumber-field/issues/11
	
        phone = to_python(42)
        self.assertEqual(phone, None)
