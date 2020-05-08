from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, null=True)
	title = models.CharField(max_length=150)
	due_date = models.DateField()
	description = models.TextField()
	active = models.BooleanField(default=True)
	verified = models.BooleanField(default=False)
	verified_at = models.DateTimeField(null=True)
	modified_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)
	recommended = models.PositiveIntegerField(default=0)
	not_recommended = models.PositiveIntegerField(default=0)
	required_amount = models.PositiveIntegerField()
	collected_amount = models.PositiveIntegerField(default=0)

class Like(models.Model):
	post = models.ForeignKey(Post, related_name='like', on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, related_name='like', on_delete=models.CASCADE, null=True)

	class Meta:
		unique_together = ('post', 'user',)

class Dislike(models.Model):
	post = models.ForeignKey(Post, related_name='unlike', on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, related_name='unlike', on_delete=models.CASCADE, null=True)

	class Meta:
		unique_together = ('post', 'user',)
