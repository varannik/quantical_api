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

    def test_create_super_user(self):
        '''Test creating super user'''
        user = get_user_model().objects.create_superuser(
            email='superuser@example.com',
            password= '@#$d520'
        )
        self.assertTrue(user.is_superuser)


    def test_new_user_email_normalized(self):
        '''Test new user email is normalaized'''
        sample_emails = [

            ['TeSt123@Example.com', 'TeSt123@example.com'],
            ['TEST123@EXAMPLE.com', 'TEST123@example.com'],
            ['Test123@Example.COM', 'Test123@example.com'],
        ]

        for email , expected in sample_emails:
            user = get_user_model().objects.create_user(email,'!@#123')
            self.assertEqual(user.email, expected)

    def test_raise_error_if_email_not_exist(self):
        '''Test if error raise when email dosent exist during user creation'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','QWS23#')


