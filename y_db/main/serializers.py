
from rest_framework import serializers
from .models import Tweet, YUser, Follow, Notification


class YUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = YUser
        fields = '__all__'
    

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = '__all__'
    
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
    
    def is_valid(self, raise_exception=False):
        valid = super(FollowSerializer, self).is_valid(raise_exception=raise_exception)
        #follwerがない場合、エラーを返す
        if 'follower' not in self.initial_data:
            self._errors['follower'] = ['This field is required.']
            return False
        #followingがない場合、エラーを返す
        elif 'following' not in self.initial_data:
            self._errors['following'] = ['This field is required.']
            return False
        #フォロワーとフォローされている人が同じ場合、エラーを返す
        elif self.initial_data['follower'] == self.initial_data['following']:
            self._errors['following'] = ['You cannot follow yourself.']
            return False
        return valid 
    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
