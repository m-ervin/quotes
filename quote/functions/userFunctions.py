# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from ..models import UserProfile

class UserFunctions(object):


    def registerUser(self, username, email, password):
        user = User.objects.create_user(username, email, password)
        user.save()

        return True
