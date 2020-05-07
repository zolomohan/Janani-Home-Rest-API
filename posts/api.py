from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from rest_framework.response import Response
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

    def partial_update(self, serializer, pk):
        post = Post.objects.get(pk=pk)
        data = self.request.data
        if(self.request.user == post.owner):
            if("active" in data):
                post.active = data['active']
            post.save()
            return Response(PostSerializer(post).data, status=202)
        return Response({"non_field_errors": "Unauthorized to perform this action."}, status=401)
