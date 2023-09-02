"""
Test For models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating user with email is successfull"""
        email = 'varanik@example.com'
        password = 'MyLove69'
        user = get_user_model().objects.create_user(

            email=email,
            password=password,

        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
