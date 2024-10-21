from django.test import TestCase, RequestFactory
from api.models import Post, Like, Follow
from django.contrib.auth.models import User
from api.serializers import UserRegistrationSerializer, PostSerializer, UserSerializer
from django.contrib.auth.models import AnonymousUser

class TestUserRegistrationSerializer(TestCase):
    def test_valid_data(self):
        data = {
            'username': 'tester',
            'email': 'tester@test.com',
            'password': 'test123'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'tester')
        self.assertEqual(user.email, 'tester@test.com')

class TestPostSerializer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user
        self.post = Post.objects.create(author=self.user, text="Test Post")
        # Criar uma curtida para testar o campo is_liked
        Like.objects.create(user=self.user, post=self.post)

    def test_valid_data(self):
        data = {
            'text': 'This is a test post'
        }
        serializer = PostSerializer(data=data, context={'request': None})
        self.assertTrue(serializer.is_valid())
        
    def test_post_serializer(self):
        self.post.refresh_from_db() 
        serializer = PostSerializer(self.post, context={'request': self.request})
        data = serializer.data
        self.assertEqual(data['text'], 'Test Post')
        self.assertEqual(data['author']['username'], 'user1')
        self.assertTrue(data['is_liked'])
        self.assertEqual(data['likes_count'], 1)
        
    def test_post_serializer_liked(self):
        self.post.refresh_from_db()
        serializer = PostSerializer(self.post, context={'request': self.request})
        data = serializer.data
        self.assertTrue(data['is_liked'])
        self.assertEqual(data['likes_count'], 1)

    def test_post_serializer_not_liked(self):
        # Remover a curtida criada do post
        Like.objects.filter(user=self.user, post=self.post).delete()
        self.post.refresh_from_db()
        serializer = PostSerializer(self.post, context={'request': self.request})
        data = serializer.data
        self.assertFalse(data['is_liked'])
        self.assertEqual(data['likes_count'], 0)

    def test_post_serializer_unauthenticated(self):
        # User não autenticado
        request = self.factory.get('/')
        request.user = AnonymousUser()
        serializer = PostSerializer(self.post, context={'request': request})
        data = serializer.data
        self.assertFalse(data['is_liked'])

    def test_post_serializer_validation(self):
        serializer = PostSerializer(data={'text': ''})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'text'})
        
    def test_post_serializer_validation_empty_text(self):
        data = {'text': ''}
        serializer = PostSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('text', serializer.errors)
        self.assertEqual(serializer.errors['text'][0], 'O texto da postagem não pode ser vazio.')
        
class TestUserSerializer(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user
        self.user_to_serialize = User.objects.create_user(username='user2', password='pass123')

    def test_user_serializer(self):
        serializer = UserSerializer(self.user_to_serialize, context={'request': self.request})
        data = serializer.data
        self.assertFalse(data['is_following'])
        self.assertEqual(data['followers_count'], 0)
        self.assertEqual(data['following_count'], 0)

    def test_user_serializer_is_following(self):
        # Cobrir linha 42: usuário está seguindo
        Follow.objects.create(follower=self.user, following=self.user_to_serialize)
        serializer = UserSerializer(self.user_to_serialize, context={'request': self.request})
        data = serializer.data
        self.assertTrue(data['is_following'])

    def test_user_serializer_unauthenticated(self):
        # User não autenticado
        request = self.factory.get('/')
        request.user = AnonymousUser()
        serializer = UserSerializer(self.user_to_serialize, context={'request': request})
        data = serializer.data
        self.assertFalse(data['is_following'])