from rest_framework import permissions

# Apenas o autor pode editar ou excluir posts.
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Todos podem ler
            return True
        return obj.author == request.user  # Apenas o autor por escrever ou excluir posts
