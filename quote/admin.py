from django.contrib import admin

# Register your models here.
from .models import UserProfile, Quote, Category, Favorite
from django.contrib.auth.models import User

admin.site.register(UserProfile)
admin.site.register(Quote)
admin.site.register(Category)
admin.site.register(Favorite)
