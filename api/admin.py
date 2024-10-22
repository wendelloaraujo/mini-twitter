from django.contrib import admin
from .models import Post, Like, Follow, Profile

# Models visible in the Django admin panel
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Profile)
