from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.response import Response
from knox.models import AuthToken
from .serializer import UserSerializer, RegisterSerializer, LoginSerializer, ProfileSerializer
from .models import Profile

# The generic views provided by REST framework allow you to quickly build API views that map closely to your database models.


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        Creates an User, stores it in the database and Authenticates the user.

        Args:
            self: Represents the instance of the class.
            request: The request itself.

        Returns:
            A dictionary containing the User information and the Authorization token. 
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Authenticates the user.

        Args:
            self: Represents the instance of the class.
            request: The request itself.

        Returns:
            A dictionary containing the User information and the Authorization token. 
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class UserAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        """
        Returns the Information of the current user who requests this endpoint.
        """
        return self.request.user


class ProfileViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        """
        Evaluvates the access permission of the various endpoints.
        Args:
            self: Represents the instance of the class.

        Returns:
           The access permission for the endpoints of this viewset.
        """
        permission_classes = []
        
        if self.action in ['retrieve']:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
