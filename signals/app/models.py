

from django.db import models

class UserProfile(models.Model):
    user = models.CharField(max_length=100)
    email = models.EmailField()
    
class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)