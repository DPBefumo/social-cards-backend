from django.test import TestCase
from users.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# Create your tests here.
class TestFollowers(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        token = Token.objects.get(user=self.user1)
        self.user2 = User.objects.create(username='user2')
        self.user3 = User.objects.create(username='user3')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    
    def test_can_follow_a_user(self):
        response = self.client.post('/api/follow/', {'user': 'user2'}, format='json')
        response = self.client.post('/api/follow/', {'user': 'user3'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['followed_user_count'], 2)
        self.assertTrue(self.user2 and self.user3 in self.user1.followed_users.all())
