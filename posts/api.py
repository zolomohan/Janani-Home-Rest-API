from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializer import PostSerializer
from django.contrib.auth.models import User
from .models import Post


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['post'], detail=True)
    def toggle(self, serializer, pk):
        post = Post.objects.get(pk=pk)
        if(self.request.user == post.owner):
            post.active = not post.active
            post.save()
            return Response(status=202)
        return Response(status=401)
