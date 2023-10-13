"""
Test for the user API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse("user:token")
ME_URL = reverse('user:me')

def create_user(**params):
    """ Create and return a new user """
    return get_user_model().objects.create_user(**params)

class PublicUserApiTest(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def create_token_for_user(self):
        """Test generates token for valid credentials"""
        payload = {
            'email':'test@example.com',
            'password': 'password123',
            'name': 'Test user'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status=status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        payload = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test User'
        }
        create_user(**payload)
        bad_credential_user ={
            'email': 'test@example.com',
            'password': 'pASSWORD121',
            'name': 'Test User'
        }
        res = self.client.post(TOKEN_URL, bad_credential_user)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_unauthorized_user(self):
        payload = {
            'email': 'test@example.com',
            'password': 'password123!',
            'name': 'Test User'
        }
        res = self.client.post(ME_URL,payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):

    def setUp(self):
        self.user = create_user(email='test@example.com',password='password123',name='Test User')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user) # We want to isolate test to just verify functionality after authentication has been done

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,{
            'email': self.user.email,
            # 'password': self.user['password'], # password is not stored in db as raw text
            'name': self.user.name
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for this end-point"""
        res = self.client.post(ME_URL,{})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user profile using PATCH/PUT"""
        payload = {
            'email': 'updated@example.com',
            'password': 'updatedpassword',
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email,payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))