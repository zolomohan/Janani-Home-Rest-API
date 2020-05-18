from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializer import UserSerializer, RegisterSerializer, LoginSerializer

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

