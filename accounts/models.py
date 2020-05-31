from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)
  dob = models.DateField()
  phone = models.CharField(max_length=15)
  phone_alt = models.CharField(max_length=15)
  gender = models.CharField(max_length=1)
  is_student = models.BooleanField()
  workplace_name = models.CharField(max_length=100)
  workplace_address = models.TextField()
  address = models.TextField()
  city = models.CharField(max_length=30)
  state = models.CharField(max_length=30)
  zipcode = models.CharField(max_length=10)
