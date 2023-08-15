from django.contrib import admin
from .models import Tweet, Follow, Notification, YUser

# Register your models here.

class TweetInline(admin.StackedInline):
    model = Tweet
    can_delete = False
    verbose_name_plural = 'Tweet'
    fk_name = 'user'

class FollowInline(admin.StackedInline):
    model = Follow
    can_delete = False
    verbose_name_plural = 'Follow'
    fk_name = 'follower'
    
class NotificationInline(admin.StackedInline):
    model = Notification
    can_delete = False
    verbose_name_plural = 'Notification'
    fk_name = 'to_user'

class YUserAdmin(admin.ModelAdmin):
    list_display = ('username', 
                    'id',
                    'email', 
                    'first_name', 
                    'last_name', 
                    'is_staff',
                    'is_active',
                    )

admin.site.register(YUser, YUserAdmin)

