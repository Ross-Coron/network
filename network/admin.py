from django.contrib import admin

# View in admin interface
from .models import User, Follow, Tweet, Like

# Register your models here.
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Tweet)
admin.site.register(Like)
