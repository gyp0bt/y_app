
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User

# Create your models here

class YUser(User):
    bio = models.TextField(blank=True)
    pic = models.ImageField(upload_to='profile_pics/', blank=True)
    
    def __str__(self):
        return self.username
    

# Tweet model
class Tweet(models.Model):
    user = models.ForeignKey(YUser, on_delete=models.CASCADE)
    content = models.TextField(max_length=280) # Based on Twitter's length
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(YUser, related_name='liked_tweets', blank=True)
    retweets = models.ManyToManyField(YUser, related_name='retweeted_tweets', blank=True)

    def __str__(self):
        return self.content


# Follow model
class Follow(models.Model):
    follower = models.ForeignKey(YUser, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(YUser, related_name='following', on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower} follows {self.following}'


# Notification model (Optional but useful)
class Notification(models.Model):
    NOTIF_TYPES = [
        ('LIKE', 'Like'),
        ('RETW', 'Retweet'),
        ('FOLL', 'Follow'),
        ('MENT', 'Mention')
    ]
    to_user = models.ForeignKey(YUser, related_name='notifications', on_delete=models.CASCADE)
    from_user = models.ForeignKey(YUser, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    notif_type = models.CharField(max_length=4, choices=NOTIF_TYPES)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.notif_type} from {self.from_user} to {self.to_user}'
