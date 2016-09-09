from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    lastName = models.CharField(max_length=30)
    firstName = models.CharField(max_length=30)
    profilePicture = models.FileField(blank=True, upload_to='profile_pictures')

    def __unicode__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Quote(models.Model):
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)
    quote = models.CharField(max_length=500)
    author = models.CharField(max_length=50)

    def __unicode__(self):
        return self.quote[:50]

class Favorite(models.Model):
    user = models.ForeignKey(User)
    quote = models.ForeignKey(Quote)

    def __unicode__(self):
        return self.user.username + " - " + self.quote.quote[:50]
