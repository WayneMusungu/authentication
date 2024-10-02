from django.test import TestCase
from drones.models import Drone
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your tests here.

class DroneModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        self.drone = Drone.objects.create(
            name = "DJI-Drone",
            description = "New DJI Drone",
            price = 39.45,
            user = self.user
        )
        
    def tearDown(self):
        self.user.delete()
        self.drone.delete()
        
    def test_drone_creation(self):
        self.assertEqual(self.drone.name, "DJI-Drone")
        self.assertEqual(self.drone.description, "New DJI Drone")
        self.assertEqual(self.drone.price, 39.45)
        self.assertEqual(self.drone.user, self.user)
        
    def test_drone_str(self):
        self.assertEqual(str(self.drone), self.drone.name)
        
    def test_drone_count(self):
        self.assertEqual(Drone.objects.count(), 1)
