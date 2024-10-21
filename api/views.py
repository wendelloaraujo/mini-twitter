from django.contrib.auth.models import User
from django.core.cache import cache
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers


from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from .models import Post, Like, Follow
from .permissions import IsAuthorOrReadOnly
from .tasks import send_follow_notification
from .serializers import PostSerializer, UserRegistrationSerializer, UserSerializer

# View para registro de usuários
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = []

# Endpoint de teste para verificar autenticação
class HelloWorldView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Hello, World!'})

# controle de taxa de requisições
class BurstRateThrottle(UserRateThrottle):
    rate = '5/minute' # Limitar a 5 requisições por minuto

# ViewSet para posts
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    throttle_classes = [BurstRateThrottle]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        # Invalida o cache quando uma nova postagem é criada
        cache_pattern = f'feed_{self.request.user.id}_page_*'
        self.invalidate_user_feed_cache(cache_pattern)

    def invalidate_user_feed_cache(self, pattern):
        keys = cache.keys(pattern)
        cache.delete_many(keys)

    # Curtir Posts
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if Like.objects.filter(user=user, post=post).exists():
            return Response({'detail': 'Você já curtiu esta postagem'}, status=status.HTTP_400_BAD_REQUEST)
        Like.objects.create(user=user, post=post)
        return Response({'status': 'Postagem curtida'})

    # Remover curtida
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like = Like.objects.filter(user=user, post=post).first()
        if like:
            like.delete()
            return Response({'status': 'Curtida removida'})
        return Response({'detail': 'Você não curtiu esta postagem.'}, status=status.HTTP_400_BAD_REQUEST)

# ViewSet para pesquisa de posts
class PostSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.select_related('author').order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', 'author__username']

# ViewSet para usuários
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.prefetch_related('followers', 'following')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Seguir usuário
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        user = request.user
        if user == user_to_follow:
            return Response({'detail': 'Você não pode seguir a si mesmo.'}, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(follower=user, following=user_to_follow).exists():
            return Response({'detail': 'Você já segue este usuário.'}, status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.create(follower=user, following=user_to_follow)
        send_follow_notification.delay(user.id, user_to_follow.id) # Enviar email de notificação
        cache_pattern = f'feed_{request.user.id}_page_*'
        self.invalidate_user_feed_cache(cache_pattern)  # Invalida o cache quando seguir alguém
        return Response({'status': f'Você agora segue {user_to_follow.username}'})

    # Deixar de Seguir um usuário
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()
        user = request.user
        follow = Follow.objects.filter(
            follower=user, following=user_to_unfollow).first()
        if follow:
            follow.delete()
            return Response({'status': f'Você deixou de seguir {user_to_unfollow.username}'})
        return Response({'detail': 'Você não segue este usuário.'}, status=status.HTTP_400_BAD_REQUEST)

    def invalidate_user_feed_cache(self, pattern):
        keys = cache.keys(pattern)
        cache.delete_many(keys)

# ViewSet para o feed de posts
class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    
    
    cache_timeout = 1  # 2 minutos
    if settings.TESTING:
        cache_timeout = 1  # 1 segundo durante os testes

    @method_decorator(vary_on_headers('Authorization'))
    @method_decorator(cache_page(cache_timeout))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.values_list(
            'following__id', flat=True)
        return Post.objects.filter(
            author__id__in=following_users
        ).select_related('author').order_by('-created_at')
