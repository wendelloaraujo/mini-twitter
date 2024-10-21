from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Post, Like, Follow
from django.core.cache import cache
# from unittest import mock

class TestUserRegistrationView(TestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'tester',
            'email': 'test@test.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class TestObtainToken(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_obtain_token(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
class TestPostViewSet(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='poster', password='testpass')
        self.client = APIClient()
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'poster', 'password': 'testpass'}, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_post(self):
        url = reverse('post-list')
        data = {
            'text': 'This is a test post'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'This is a test post')

    def test_like_post(self):
        post = Post.objects.create(author=self.user, text='A post to like')
        url = reverse('post-like', kwargs={'pk': post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Postagem curtida')
        
    def test_unlike_post(self):
        # Primeiro, curtir o post
        post = Post.objects.create(author=self.user, text='A post to unlike')
        Like.objects.create(user=self.user, post=post)
        url = reverse('post-unlike', kwargs={'pk': post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Curtida removida')
        
    def test_like_post_already_liked(self):
        # usuário já curtiu o post
        post = Post.objects.create(author=self.user, text='A post to like')
        Like.objects.create(user=self.user, post=post)
        url = reverse('post-like', kwargs={'pk': post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Você já curtiu esta postagem')
        
    def test_unlike_post_not_liked(self):
        # usuário não curtiu o post
        post = Post.objects.create(author=self.user, text='A post to unlike')
        url = reverse('post-unlike', kwargs={'pk': post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Você não curtiu esta postagem.')

class TestUserViewSet(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.client = APIClient()
        # Autenticar como user1
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'user1', 'password': 'pass123'}, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_follow_user(self):
        url = reverse('user-follow', kwargs={'pk': self.user2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], f'Você agora segue {self.user2.username}')

    def test_unfollow_user(self):
        # Primeiro, seguir o usuário
        Follow.objects.create(follower=self.user1, following=self.user2)
        url = reverse('user-unfollow', kwargs={'pk': self.user2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], f'Você deixou de seguir {self.user2.username}')
        
    def test_follow_self(self):
        # usuário tentando seguir a si mesmo
        url = reverse('user-follow', kwargs={'pk': self.user1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Você não pode seguir a si mesmo.')

    def test_unfollow_user_not_following(self):
        # usuário tentando deixar de seguir alguém que não segue
        url = reverse('user-unfollow', kwargs={'pk': self.user2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Você não segue este usuário.')
        
    def test_follow_user_already_following(self):
        # user1 já segue user2
        Follow.objects.create(follower=self.user1, following=self.user2)
        # Tenta seguir novamente
        url = reverse('user-follow', kwargs={'pk': self.user2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Você já segue este usuário.')

class TestFeedViewSet(TestCase):
    def setUp(self):
        cache.clear()
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.user3 = User.objects.create_user(username='user3', password='pass123')

        self.client = APIClient()
        # Autenticar como user1
        response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'user1', 'password': 'pass123'},
            format='json'
        )
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def tearDown(self):
        cache.clear()
        Post.objects.all().delete()
        Follow.objects.all().delete()

    def test_get_feed(self):
        # user1 segue user2
        Follow.objects.create(follower=self.user1, following=self.user2)
        # Criar um post de user2
        Post.objects.create(author=self.user2, text='Post from user2')

        url = reverse('feed-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['text'], 'Post from user2')

    def test_feed_cache(self):
        # user1 segue user2
        Follow.objects.create(follower=self.user1, following=self.user2)

        # Criar um post de user2
        Post.objects.create(author=self.user2, text='Post from user2')

        url = reverse('feed-list')

        # Primeira requisição (cache miss)
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data['results']), 1)

        # Criar um novo post de user2
        Post.objects.create(author=self.user2, text='New post from user2')

        # Segunda requisição dentro do tempo de cache
        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data['results']), 1)  # Ainda deve ser 1 devido ao cache

        # Aguarda o cache expirar (1 segundo)
        import time
        time.sleep(1.1)

        # Terceira requisição após o cache expirar
        response3 = self.client.get(url)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response3.data['results']), 2)  # Agora deve ser 2 posts

    def test_feed_no_following(self):
        url = reverse('feed-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Como user1 não está seguindo ninguém, o feed deve estar vazio
        self.assertEqual(len(response.data['results']), 0)

    def test_feed_following_users(self):
        # user1 segue user2
        Follow.objects.create(follower=self.user1, following=self.user2)

        # Criar um post de user2
        Post.objects.create(author=self.user2, text='Post from user2')

        url = reverse('feed-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['text'], 'Post from user2')

        
class TestHelloWorldView(TestCase):
    def test_hello_world_authenticated(self):
        # chamada ao endpoint hello/
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpass'}, format='json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('hello_world')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Hello, World!'})