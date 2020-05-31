from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from accounts.serializer import UserSerializer
from .serializer import PostSerializer, LikeSerializer, DislikeSerializer, CommentSerializer
from django.contrib.auth.models import User
from .models import Post, Like, Dislike, Comment

# Django REST framework allows you to combine the logic for a set of related views in a single class, called a ViewSet.
# A ViewSet class is simply a type of class-based View, that does not provide any method handlers such as .get() or .post(), 
# and instead provides actions such as .list() and .create().

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_permissions(self):
        """
        Evaluvates the access permission of the various endpoints.
        Args:
            self: Represents the instance of the class.

        Returns:
           The access permission for the endpoints of this viewset.
        """

        if self.action in ['list', 'retrieve', 'comment', 'active']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


    def perform_create(self, serializer):
        """
        Saves the user who creates the Post along with other fields.
        The user is determined from the Authorization header of the request.

        Args:
            self: Represents the instance of the class.
            serializer: The serializer of the model.
        """

        serializer.save(owner=self.request.user)

    # TODO: Paginate the response.
    def list(self, serializer):
        """
        Endpoint for list of posts in the database.

        Args:
            self: Represents the instance of the class.
            serializer: The serializer of the model.
        """

        post = Post.objects.filter(active=True)
        data = PostSerializer(post, many=True).data

        # The response is populated with the Post owner's information before response.
        for post in data:
            post['owner'] = User.objects.get(pk=post['owner']).username
        return Response(data)

    @action(methods=['get'], detail=True)
    def active(self, serializer, pk):
        """
        Endpoint for list of posts created by a certain user.

        Args:
            self: Represents the instance of the class.
            serializer: The serializer of the model.
        """
        user = User.objects.get(username=pk)
        post = Post.objects.filter(active=True, owner=user)
        data = PostSerializer(post, many=True).data

        # The response is populated with the Post owner's information before response.
        for post in data:
            post['owner'] = User.objects.get(pk=post['owner']).username
        return Response(data)

    @action(methods=['get'], detail=True)
    def disabled(self, serializer, pk):
        """
        Endpoint for list of posts disabled by a certain user.

        Args:
            self: Represents the instance of the class.
            serializer: The serializer of the model.
        """
        if(self.request.user.username == pk):
            user = User.objects.get(username=pk)
            post = Post.objects.filter(active=False, owner=user)
            data = PostSerializer(post, many=True).data

            # The response is populated with the Post owner's information before response.
            for post in data:
                post['owner'] = User.objects.get(pk=post['owner']).username
            return Response(data)
        return Response({"detail": "You are not authorized to access this data."}, status=401)

    # This function is used to respond with the requested post. The post is requested using the Post's ID.
    def retrieve(self, serializer, pk):
        """
        Endpoint for a single post in the database.

        Args:
            self: Represents the instance of the class.
            serializer: The serializer of the model.
            pk: Primary key of the post.

        Return:
            Requested post data along with the post owner's information.
        """

        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist in the database."}, status=400)
        
        if(post.owner != self.request.user and not post.active):
            return Response({"error": "Post has been disabled by the user."}, status=400)

        data = PostSerializer(post).data
        # The response is populated with the Post owner's information before response.
        data['owner'] = post.owner.username

        # The response is populated with the number of likes and dislikes before response.
        data['likes'] = Like.objects.filter(post=post).count()
        data['dislikes'] = Dislike.objects.filter(post=post).count()

        # The response is populated with whether the user who requested it has liked or disliked the Post.
        # If the request is not authenticated, then this part is skipped.
        if(self.request.auth):
            try:
                liked = Like.objects.get(user=self.request.user, post=post)
                data['user_liked'] = True
            except Like.DoesNotExist:
                data['user_liked'] = False
            try:
                disliked = Dislike.objects.get(user=self.request.user, post=post)
                data['user_disliked'] = True
            except Dislike.DoesNotExist:
                data['user_disliked'] = False
        return Response(data)

    @action(methods=['post'], detail=True)
    def toggle(self, serializer, pk):
        """
        Endpoint for toggling the post between Active/Disabled. 
        This endpoint is a protected endpoint. Only the owner of the post can access this endpoint.

        Args:
            self: Represents the instance of the class.
            serializer: The serializer of the model.
            pk: Primary key of the post.

        Return:
            Response code of 200 (OK) if the task is completed. Else, 401 (Unauthorized) if an unauthorized user requests it.
        """
        post = Post.objects.get(pk=pk)

        # Checks whether the user who requested this endpoint is the same as the owner of the post.
        if(self.request.user == post.owner):
            post.active = not post.active
            post.save()
            return Response(status=200)
        return Response(status=401)

    @action(methods=['post'], detail=True)
    def like(self, serializer, pk):
        """
        Endpoint for liking the post. 
        If the user who likes the post has already disliked it, the Dislike entry is removed from the database.

        Args:
            self: Represents the instance of the class.
            serializer: The serializer of the model.
            pk: Primary key of the post.

        Return:
            Response code of 200 (OK) if the task is completed.
        """
        post = Post.objects.get(pk=pk)

        # Deletes the dislike entry in the database if it exists.
        try:
            Dislike.objects.get(user=self.request.user, post=post).delete()
        except Dislike.DoesNotExist:
            pass

        # A new like entry is created in the Database.
        Like(post=post, user=self.request.user).save()
        return Response(status=200)

    # ENDPOINT: Used to remove a like of the post.
    @action(methods=['post'], detail=True)
    def removelike(self, serializer, pk):
        """
        Endpoint for remove a like of a post. 

        Args:
            self: Represents the instance of the class.
            serializer: The serializer of the model.
            pk: Primary key of the post.

        Return:
            Response code of 200 (OK) if the task is completed.
        """
        post = Post.objects.get(pk=pk)
        Like.objects.get(post=post, user=self.request.user).delete()
        return Response(status=200)

    # ENDPOINT: Used to dislike the post.
    @action(methods=['post'], detail=True)
    def dislike(self, serializer, pk):
        """
        Endpoint for disliking the post.
        If the user who likes the post has already liked it, the Like entry is removed from the database.

        Args:
            self: Represents the instance of the class.
            serializer: The serializer of the model.
            pk: Primary key of the post.

        Return:
            Response code of 200 (OK) if the task is completed.
        """
        post = Post.objects.get(pk=pk)

        # Deletes the like entry in the database if it exists.
        try:
            Like.objects.get(user=self.request.user, post=post).delete()
        except Like.DoesNotExist:
            pass

        # A new dislike entry is created in the Database.
        Dislike(post=post, user=self.request.user).save()
        return Response(status=200)

    # ENDPOINT: Used to remove a dislike of the post.
    @action(methods=['post'], detail=True)
    def removedislike(self, serializer, pk):
        """
        Endpoint for removing a dislike of a post.
        If the user who likes the post has already liked it, the Like entry is removed from the database.

        Args:
            self: Represents the instance of the class.
            serializer: The serializer of the model.
            pk: Primary key of the post.

        Return:
            Response code of 200 (OK) if the task is completed.
        """
        post = Post.objects.get(pk=pk)
        Dislike.objects.get(post=post, user=self.request.user).delete()
        return Response(status=200)

    @action(methods=['post', 'get'], detail=True)
    def comment(self, serializer, pk):
        """
        This method serves as two endpoints.
        1. GET: The method returns all the comments of the requested post.
        2. POST: The method created a new comment and stores it in the databse.

        Args:
            self: Represents the instance of the class.
            serializer: The serializer of the model.
            pk: Primary key of the post.

        Return:
            Response code of 400 (Bad Request) if the post is disabled.
            GET: 
                The serialized data of the list of comments associated to the post.
            POST:
                The newly created comment data along with a status code of 200 (OK).
                or
                Response code of 401 (Unauthorized) if the user is not authenticated.
        """

        # Checks whether the post is active.
        post = Post.objects.get(pk=pk)
        if(not post.active):
            return Response({"error": "Post does not exist in the database."}, status=400)

        # TODO: Paginate the response
        # 1. GET: The comments are fetched from the database. 
        if self.request.method == 'GET':
            comments = Comment.objects.filter(post=post, disabled=False)
            serializer = CommentSerializer(comments, many=True)

            # The user information of the respective comments are populated before response.
            for comment in serializer.data:
                comment['user'] = User.objects.get(pk=comment['user']).username
            return Response(serializer.data)

        # 2. POST: The request is checked for authentication. 
        # If the request is authenticated, a new entry in the database is created.
        elif self.request.method == 'POST':
            if self.request.auth != None:
                comment = Comment(post=post, user=self.request.user, body=self.request.data['comment'])
                comment.save()
                return Response(CommentSerializer(comment).data, status=200)
            return Response(status=401)

    # ENDPOINT: Used to disable a comment. The disabled attribute is set to True.
    # This endpoint is a protected endpoint. Only the owner of the post can access this endpoint.
    @action(methods=['post'], detail=False)
    def disablecomment(self, serializer):
        """
        This endpoint is used to disable a comment. The disabled attribute is set to True.
        The body of the request must contain the ID of the comment that has to be disabled.
        Args:
            self: Represents the instance of the class.
            serializer: The serializer of the model.

        Return:
            Response code of 400 (Bad Request) if the comment is already disabled.
            or
            Response code of 401 (Unauthorized) if the user is not the owner of the comment.
            or
            Response code of 200 (OK) if the task is completed.
        """
        comment = Comment.objects.get(id=self.request.data['id'])

        # Checks if the comment has already been disabled.
        if(comment.disabled):
            return Response({"error": "Comment Not Found, Might be disabled already."}, status=400)
        
        # Checks whether the user who requested this endpoint is the same as the owner of the comment.
        if(comment.user != self.request.user):
            return Response(status=401)

        # Sets the value of the Disabled field to True and saves it.
        comment.disabled = True
        comment.save()
        return Response(status=200)
