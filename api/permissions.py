from rest_framework import permissions

# Only the author can edit or delete posts.
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Everyone can read
            return True
        return obj.author == request.user  # Only the author can write or delete posts
