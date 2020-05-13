from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes 
# that can then be easily rendered into JSON, XML or other content types. 
# Serializers also provide deserialization, allowing parsed data to be converted back into complex types, 
# after first validating the incoming data. 

# The Meta class is used to specify the Model and the fields in the model that needs to be serialized/deserialized.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    
    def create(self, credentials):
        """
        Creates an User and stores it in the database.

        Args:
            self: Represents the instance of the class.
            credentials: The credentials given by the user.
            
        Returns:
            The user who was created and stored in the database.
        """
        return User.objects.create_user(
            credentials['username'],
            credentials['email'],
            credentials['password']
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, credentials):
        """
        This method is used to validate the user credentials. 

        Args:
            self: Represents the instance of the class.
            credentials: The credentials given by the user.
            
        Returns:
            If the credentials are valid, a Auth Token is returned, else a validation error is returned.
        """
        user = authenticate(**credentials)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials')
