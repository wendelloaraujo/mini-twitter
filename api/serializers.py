from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Like, Follow, Profile

# Registro de usuário
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

# Detalhes do usuário
class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='profile.followers_count', read_only=True)
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'followers_count',
                  'following_count', 'is_following')
        read_only_fields = ('followers_count', 'following_count')

    # Total de pessoas que o usuário segue
    def get_following_count(self, obj):
        return obj.following.count()

    # Verificar se esta seguindo um usuário especifico
    def get_is_following(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Follow.objects.filter(follower=user, following=obj).exists()
        return False

# Posts
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    text = serializers.CharField(max_length=280, allow_blank=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'image',
                  'created_at', 'likes_count', 'is_liked')
        read_only_fields = ('likes_count',)

    # Verificar se o texto não está vazio
    def validate_text(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("O texto da postagem não pode ser vazio.")
        return value

    # Verificar se um post especifico foi curtido pelo usuário
    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Like.objects.filter(user=user, post=obj).exists()
        return False

# Likes
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created_at')

# Follow
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'created_at')
