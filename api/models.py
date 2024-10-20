from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

#Model de perfil
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    followers_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

#Model de post
class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(max_length=280) # Limite de caracteres igual ao Twitter
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveIntegerField(default=0)  # Contador de Likes

    def __str__(self):
        return f'{self.author.username}: {self.text[:50]}'

#Model de like
class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='liked_posts')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post') # Somente uma curtida por usuário em cada post.

    def __str__(self):
        return f'{self.user.username} liked {self.post.id}'

# Model de follow
class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following') # Impedir de seguir o mesmo usuário duas vezes
        constraints = [
            models.CheckConstraint(check=~models.Q(
                follower=models.F('following')), name='prevent_self_follow') # Impedir de seguir a si mesmo
        ]

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'

# Criar ou atualizar perfil
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) # Criar se for um perfil novo
    else:
        instance.profile.save() # Salvar se for um perfil existente.

# Contagem de seguidores
@receiver(post_save, sender=Follow)
def increment_followers_count(sender, instance, created, **kwargs):
    if created:
        profile = instance.following.profile
        profile.followers_count = models.F('followers_count') + 1
        profile.save()


@receiver(post_delete, sender=Follow)
def decrement_followers_count(sender, instance, **kwargs):
    profile = instance.following.profile
    profile.followers_count = models.F('followers_count') - 1
    profile.save()

# Contagem de likes
@receiver(post_save, sender=Like)
def increment_likes_count(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        post.likes_count = models.F('likes_count') + 1
        post.save()


@receiver(post_delete, sender=Like)
def decrement_likes_count(sender, instance, **kwargs):
    post = instance.post
    post.likes_count = models.F('likes_count') - 1
    post.save()