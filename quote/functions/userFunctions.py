# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from ..models import UserProfile

class UserFunctions(object):


    def registerUser(self, username, email, password, firstName, lastName):
        user = User.objects.create_user(username, email, password)
        user.save()

        profile = UserProfile(user = user, firstName = firstName, lastName = lastName)
        profile.save()

        return True

    def modifyUserProfile(self, user, formData):
        user = User.objects.get(id = user.id)
        user.username = formData['username']
        user.email = formData['email']
        user.save()

        profile, p = UserProfile.objects.get_or_create(user = user)
        profile.firstName = formData['firstName']
        profile.lastName = formData['lastName']
        profile.save()

        return True

    def uploadProfilePicture(self, user, picture):

        print(picture)
        profile, p = UserProfile.objects.get_or_create(user = user)
        profile.profilePicture = picture
        # picture.save()

        return True
