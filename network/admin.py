from django.contrib import admin

# View in admin interface
from .models import User, Follow, Tweet #, Like

# Show DateTimeField (typically hidden from admin page)
class TweetAdmin(admin.ModelAdmin):
    readonly_fields = ('posted',)

# Register your models here.
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Tweet, TweetAdmin)
#admin.site.register(Like)
