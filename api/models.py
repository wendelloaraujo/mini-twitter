from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    followers_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

# Post model
class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(max_length=280, blank=True) # Character limit similar to Twitter
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveIntegerField(default=0)  # Like counter

    def __str__(self):
        return f'{self.author.username}: {self.text[:50]}'

# Like model
class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='liked_posts')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post') # Only one like per user on each post

    def __str__(self):
        return f'{self.user.username} liked {self.post.id}'

# Follow model
class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following') # Prevent following the same user twice
        constraints = [
            models.CheckConstraint(condition=~models.Q(
                follower=models.F('following')), name='prevent_self_follow') # Prevent following oneself
        ]

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'

# Create or update profile
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) # Create if it's a new profile
    else:
        instance.profile.save() # Save if it's an existing profile

# Follower count
@receiver(post_save, sender=Follow)
def increment_followers_count(sender, instance, created, **kwargs):
    if created:
        Profile.objects.filter(pk=instance.following.profile.pk).update(followers_count=F('followers_count') + 1)

@receiver(post_delete, sender=Follow)
def decrement_followers_count(sender, instance, **kwargs):
    Profile.objects.filter(pk=instance.following.profile.pk).update(followers_count=F('followers_count') - 1)

# Like count
@receiver(post_save, sender=Like)
def increment_likes_count(sender, instance, created, **kwargs):
    if created:
        Post.objects.filter(pk=instance.post.pk).update(likes_count=F('likes_count') + 1)

@receiver(post_delete, sender=Like)
def decrement_likes_count(sender, instance, **kwargs):
    Post.objects.filter(pk=instance.post.pk).update(likes_count=F('likes_count') - 1)