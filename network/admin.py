from django.contrib import admin

# To view models in admin interface
from .models import User, Follow, Tweet

# Show DateTimeField (typically hidden from admin page)
class TweetAdmin(admin.ModelAdmin):
    readonly_fields = ('posted',)

# Register your models here.
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Tweet, TweetAdmin)