from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .serializer import PostSerializer, LikeSerializer, DislikeSerializer
from django.contrib.auth.models import User
from .models import Post, Like, Dislike


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

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
            return Response(status=200)
        return Response(status=401)

    @action(methods=['post'], detail=True)
    def like(self, serializer, pk):
        post = Post.objects.get(pk=pk)
        try:
            Dislike.objects.get(user=self.request.user, post=post).delete()
        except Dislike.DoesNotExist:
            pass
        like = Like(post=post, user=self.request.user)
        like.save()
        return Response(status=200)

    @action(methods=['post'], detail=True)
    def removelike(self, serializer, pk):
        post = Post.objects.get(pk=pk)
        Like.objects.get(post=post, user=self.request.user).delete()
        return Response(status=200)

    @action(methods=['post'], detail=True)
    def dislike(self, serializer, pk):
        post = Post.objects.get(pk=pk)
        try:
            Like.objects.get(user=self.request.user, post=post).delete()
        except Like.DoesNotExist:
            pass
        dislike = Dislike(post=post, user=self.request.user)
        dislike.save()
        return Response(status=200)

    @action(methods=['post'], detail=True)
    def removedislike(self, serializer, pk):
        post = Post.objects.get(pk=pk)
        Dislike.objects.get(post=post, user=self.request.user).delete()
        return Response(status=200)

    @action(methods=['get'], detail=True)
    def likestatus(self, serializer, pk):
        post = Post.objects.get(pk=pk)
        liked = None
        disliked = None
        try:
            like = Like.objects.get(user=self.request.user, post=post)
            return Response({"liked": True})
        except Like.DoesNotExist:
            pass

        try:
            dislied = Dislike.objects.get(user=self.request.user, post=post).delete()
            return Response({"disliked": True})
        except Dislike.DoesNotExist:
            pass
        return Response({"liked": False, "disliked": False})