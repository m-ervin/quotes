from django.contrib.auth.models import User
from ..models import UserProfile
from django.utils.crypto import get_random_string

class UserFunctions:

    def registerUser(username, email, password):
        user = User.objects.create_user(username, email, password)
        user.is_active = False
        activationString = get_random_string(length=30)

        while(UserProfile.objects.filter(activationString = activationString).exists()):
                activationString = get_random_string(length=30)
        profile = UserProfile(user = user, activationString= activationString)
        profile.save()
        user.save()
