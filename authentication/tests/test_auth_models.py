from django.test import TestCase
from authentication.models import User


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        
    def tearDown(self):
        self.user.delete()
        
    def test_user_creation(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.user.check_password('testpass123'))
        
    def test_user_str(self):
        user = User.objects.get(email='testuser@example.com')
        self.assertEqual(str(user), user.email)
        
    def test_user_count(self):
        user = User.objects.count()
        self.assertEqual(user, 1)
        
        