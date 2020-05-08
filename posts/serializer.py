from rest_framework import serializers
from .models import Post, Like, Dislike

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