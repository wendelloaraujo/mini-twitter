from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Post
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

# The method names represent what is being tested.
class TestPermissions(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.post = Post.objects.create(author=self.user1, text="First Post")
        self.client = APIClient()
        
    def test_read_permission(self):
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_author_can_edit_post(self):
        # Get JWT token for user1
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'user1', 'password': 'pass123'}, format='json')
        token = response.data['access']
        # Set the token in the authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        url = reverse('post-detail', kwargs={'pk': self.post.id})
        data = {'text': 'Updated Post'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_author_cannot_edit_post(self):
        # Get JWT token for user2
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'user2', 'password': 'pass123'}, format='json')
        token = response.data['access']
        # Set the token in the authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        url = reverse('post-detail', kwargs={'pk': self.post.id})
        data = {'text': 'Hacked Post'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

