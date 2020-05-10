from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from accounts.serializer import UserSerializer
from .serializer import PostSerializer, LikeSerializer, DislikeSerializer, CommentSerializer
from django.contrib.auth.models import User
from .models import Post, Like, Dislike, Comment


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'likecount', 'comment']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, serializer):
        post = Post.objects.filter(active=True)
        data = PostSerializer(post, many=True).data
        for post in data:
            post['owner'] = User.objects.get(pk=post['owner']).username
        return Response(data)

    def retrieve(self, serializerm, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist in the database."}, status=400)
        if(post.owner != self.request.user and not post.active):
            return Response(status=401)
        data = PostSerializer(post).data
        data['owner'] = post.owner.username
        return Response(data)

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
    def likecount(self, serializer, pk):
        post = Post.objects.get(pk=pk)
        likes = Like.objects.filter(post=post).count()
        dislikes = Dislike.objects.filter(post=post).count()
        return Response({"likes": likes, "dislikes": dislikes})

    @action(methods=['get'], detail=True)
    def userpostlike(self, serializer, pk):
        post = Post.objects.get(pk=pk)
        try:
            liked = Like.objects.get(user=self.request.user, post=post)
            return Response({"liked": True})
        except Like.DoesNotExist:
            pass

        try:
            disliked = Dislike.objects.get(user=self.request.user, post=post)
            return Response({"disliked": True})
        except Dislike.DoesNotExist:
            pass
        return Response({"liked": False, "disliked": False})

    @action(methods=['post', 'get'], detail=True)
    def comment(self, serializer, pk):
        post = Post.objects.get(pk=pk)
        if self.request.method == 'POST':
            if self.request.auth != None:
                comment = Comment(post=post, user=self.request.user, body=self.request.data['comment'])
                comment.save()
                return Response(CommentSerializer(comment).data, status=200)
            return Response(status=401)
        elif self.request.method == 'GET':
            comments = Comment.objects.filter(post=post, disabled=False)
            serializer = CommentSerializer(comments, many=True)
            for comment in serializer.data:
                comment['user'] = User.objects.get(pk=comment['user']).username
            return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def disablecomment(self, serializer):
        comment = Comment.objects.get(id=self.request.data['id'])
        if(comment.disabled):
            return Response({"error": "Comment Not Found, Might be disabled already."}, status=400)
        if(comment.user != self.request.user):
            return Response(status=401)
        comment.disabled = True
        comment.save()
        return Response(status=200)
