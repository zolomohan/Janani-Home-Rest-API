from rest_framework import viewsets, permissions
from .models import Post
from .serializer import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
