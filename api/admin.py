from django.contrib import admin
from .models import Post, Like, Follow, Profile

# Modelo visiveis no painel de administração do Django
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Profile)
