from django.contrib import admin

# Register your models here.
from .models import UserProfile, Quote, Category, Favorite

admin.site.register(UserProfile)
admin.site.register(Quote)
admin.site.register(Category)
admin.site.register(Favorite)
