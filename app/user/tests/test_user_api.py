"""
Test create user API
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

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

  def test_create_token_for_user(self):
      """ Test Token is generated for valid credentials. """
      user_detail = {
         'name' : 'Test',
         'email' : 'test1@example.com',
         'password': 'ececseve58'
      }

      create_user(**user_detail)
      payload = {
         'email':user_detail['email'],
         'password':user_detail['password']
      }

      res = self.client.post(TOKEN_URL, payload)
      self.assertIn('token' , res.data)
      self.assertEqual(res.status_code, status.HTTP_200_OK)

  def test_create_token_bad_credential(self):
     """Test token is not in response for invalid request"""
     user_details = {
         'name' : 'Test2',
         'email' : 'test3@example.com',
         'password': 'ececseve58'
     }
     create_user(**user_details)

     payload = {
        'email' : 'test3@example.com',
        'password':'54548dwde'
     }
     res = self.client.post(TOKEN_URL, payload)
     self.assertNotIn('token', res.data)
     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_token_blank_password(self):
     """Test token is not created for blank password"""
     payload = {'email': 'test@example.com' , 'password': ''}
     res = self.client.post(TOKEN_URL, payload)
     self.assertNotIn('token', res.data)
     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


  def test_retrieve_user_unauthorized(self):
     """Test authentication is required for users."""
     res = self.client.get(ME_URL)

     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTest(TestCase):
   """Test API requests that requires authentication."""

   def setUp(self):
      self.user = create_user(
         email = "test123@example.com",
         password = "test12345#",
         name = "Ali"
      )
      self.client = APIClient()
      self.client.force_authenticate(user=self.user)

   def test_retriev_profile_success(self):
      """Test retrieving profile for logged user"""

      res = self.client.get(ME_URL)

      self.assertEqual(res.status_code, status.HTTP_200_OK)
      self.assertEqual(res.data, {
         'name': self.user.name,
         'email':self.user.email
      })

   def test_post_me_is_not_allowed(self):
      """Test Post is not allowed for ME URL"""
      res = self.client.post(ME_URL, {})

      self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

   def test_update_user_profile(self):
      """Test updating the user profile for the authenticated user."""
      payload = {'name':'asgar updated', 'password':'NewwPaasAsgar'}

      res = self.client.patch(ME_URL, payload)
      print(res)
      self.user.refresh_from_db()
      self.assertEqual(self.user.name, payload['name'])
      self.assertTrue(self.user.check_password(payload['password']))
      self.assertEqual(res.status_code, status.HTTP_200_OK)

