from django.test import TestCase
from django.contrib.auth.models import User
from api.models import Post, Like, Follow, Profile

# The method names represent what is being tested.
class TestPostModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_post(self):
        post = Post.objects.create(author=self.user, text='Test post')
        self.assertEqual(post.author.username, 'testuser')
        self.assertEqual(post.text, 'Test post')
        self.assertEqual(post.likes_count, 0)

class TestLikeModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='liker', password='testpass')
        self.post = Post.objects.create(author=self.user, text='Another post')

    def test_like_post(self):
        like = Like.objects.create(user=self.user, post=self.post)
        self.assertEqual(like.user.username, 'liker')
        self.assertEqual(like.post.text, 'Another post')
        
class TestFollowModel(TestCase):
    def setUp(self):
        self.follower = User.objects.create_user(username='follower', password='testpass')
        self.following = User.objects.create_user(username='following', password='testpass')

    def test_follow_user(self):
        follow = Follow.objects.create(follower=self.follower, following=self.following)
        self.assertEqual(follow.follower.username, 'follower')
        self.assertEqual(follow.following.username, 'following')
        
class TestModels(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.post = Post.objects.create(author=self.user1, text="First Post")
    
    # Check if the profile is created automatically  
    def test_profile_creation(self):
        self.assertTrue(Profile.objects.filter(user=self.user1).exists())
        
    def test_profile_str(self):
        profile = self.user1.profile
        self.assertEqual(str(profile), self.user1.username)
    
    def test_post_str(self):
        expected_str = f'{self.user1.username}: {self.post.text[:50]}'
        self.assertEqual(str(self.post), expected_str)

    def test_like_str(self):
        like = Like.objects.create(user=self.user2, post=self.post)
        expected_str = f'{self.user2.username} liked {self.post.id}'
        self.assertEqual(str(like), expected_str)

    def test_follow_str(self):
        follow = Follow.objects.create(follower=self.user2, following=self.user1)
        expected_str = f'{self.user2.username} follows {self.user1.username}'
        self.assertEqual(str(follow), expected_str)

    def test_profile_update(self):
        self.user1.email = 'newemail@example.com'
        self.user1.save()
        self.assertEqual(self.user1.profile.user.email, 'newemail@example.com')

    def test_follow_increment(self):
        Follow.objects.create(follower=self.user2, following=self.user1)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.profile.followers_count, 1)

    def test_unfollow_decrement(self):
        follow = Follow.objects.create(follower=self.user2, following=self.user1)
        follow.delete()
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.profile.followers_count, 0)

    def test_like_increment(self):
        Like.objects.create(user=self.user2, post=self.post)
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes_count, 1)

    def test_unlike_decrement(self):
        like = Like.objects.create(user=self.user2, post=self.post)
        like.delete()
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes_count, 0)