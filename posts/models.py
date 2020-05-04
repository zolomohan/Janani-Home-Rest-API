from django.db import models

class Post(models.Model):
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