from rest_framework import serializers
from .models import Post, Like, Dislike, Comment

# Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes 
# that can then be easily rendered into JSON, XML or other content types. 
# Serializers also provide deserialization, allowing parsed data to be converted back into complex types, 
# after first validating the incoming data. 

# The Meta class is used to specify the Model and the fields in the model that needs to be serialized/deserialized.

class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Like
    fields = '__all__'

class DislikeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Dislike
    fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'