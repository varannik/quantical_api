"""
Test create user API
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
  '''Test the public features of user API'''

  def setUp(self):
     self.client= APIClient()

  def test_user_is_created(self):
      '''Test user is created successfuly'''

      payload = {
          'email' : 'test@example.com',
          'password' : 'QWE1234d52',
          'name' : 'Reza'
      }
      res = self.client.post(CREATE_USER_URL, payload)
      self.assertEqual(res.status_code, status.HTTP_201_CREATED)
      user = get_user_model().objects.get(email=payload['email'])
      self.assertTrue(user.check_password(payload['password']))
      self.assertNotIn('password',res.data)

  def test_user_exist_error(self):
     '''Test new user is not registerd user'''

     payload = {
        'email' : 'test@example.com',
        'password' : '@#$233$MCC',
        'name' : 'Reza'
     }
     create_user(**payload)
     res = self.client.post(CREATE_USER_URL, payload)
     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_password_is_too_short_error(self):
     '''Test password is too short less than 8 character'''

     payload = {
        'email' : 'test@example.com',
        'password' : '@#',
        'name' : 'Reza'
     }
     res = self.client.post(CREATE_USER_URL, payload)
     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
     user_exist = get_user_model().objects.filter(
        email = payload['email']
     ).exists()
     self.assertFalse(user_exist)

