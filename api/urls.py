from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, HelloWorldView, PostViewSet, UserViewSet, FeedViewSet, PostSearchViewSet
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'users', UserViewSet, basename='user')
router.register(r'feed', FeedViewSet, basename='feed')
router.register(r'search', PostSearchViewSet, basename='search')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', HelloWorldView.as_view(), name='hello_world'),
] + router.urls
