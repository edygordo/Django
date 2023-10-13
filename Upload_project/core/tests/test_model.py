"""
Test for custom user model and it's userManager
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from decimal import Decimal

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'user@example.com'
        password = 'password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        test_emails = ['user1@exAmple.com','user2@EXAMPLE.cOM']
        for email in test_emails:
            user = get_user_model().objects.create_user(email, 'test123')
            self.assertEqual(user.email, email.lower())
            
    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_recipe(self):
        """Test creating a new recipe"""
        user = get_user_model().objects.create_user(email='test@example.com', password='testpass123')
        recipe = models.Recipe.objects.create(user=user,title='Sample recipe name',time_minutes=5,
                                              price = Decimal('5.5'),description='Sample recipe description')
        
        self.assertEqual(str(recipe),'Sample recipe name')
        