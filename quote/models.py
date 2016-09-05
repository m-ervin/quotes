from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    activationString = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username
