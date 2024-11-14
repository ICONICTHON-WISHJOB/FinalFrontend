from django.test import TestCase
from .models import CustomUser

class SignupTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(username='testuser', password='password123')
        self.assertEqual(user.username, 'testuser')