
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Tweet, YUser, Follow, Notification
from .serializers import TweetSerializer, YUserSerializer, FollowSerializer, NotificationSerializer


class YUserViewSet(viewsets.ModelViewSet):
    queryset = YUser.objects.all()
    serializer_class = YUserSerializer

    def create(self, request, *args, **kwargs):
        #ユーザーネームがない場合、エラーを返す
        if 'username' not in request.data:
            return Response({'error': 'Username is required.'}, status=400)
        #パスワードがない場合、エラーを返す
        elif 'password' not in request.data:
            return Response({'error': 'Password is required.'}, status=400)
        #メールアドレスがない場合、エラーを返す
        elif 'email' not in request.data:
            return Response({'error': 'Email is required.'}, status=400)
        #ユーザーネームが被っている場合、エラーを返す
        elif YUser.objects.filter(username=request.data['username']).exists():
            return Response({'error': 'Password is incorrect.'}, status=400)
        #メールアドレスが被っている場合、エラーを返す
        elif YUser.objects.filter(email=request.data['email']).exists():
            return Response({'error': 'Email is incorrect.'}, status=400)
        #ユーザーIDが被っている場合、エラーを返す
        elif 'id' in request.data and YUser.objects.filter(pk=request.data['id']).exists():
            return Response({'error': 'ID is incorrect.'}, status=400)
        #ユーザーIDがない場合、ユーザーIDを作成する
        elif 'id' not in request.data:
            request.data['id'] = YUser.objects.all().count() + 1
            while YUser.objects.filter(pk=request.data['id']).exists():
                request.data['id'] += 1
        return super(YUserViewSet, self).create(request, *args, **kwargs)
        

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def create(self, request, *args, **kwargs):
        #ツイート内容がない場合、エラーを返す
        if 'content' not in request.data:
            return Response({'error': 'Content is required.'}, status=400)
        #ユーザーIDがない場合、エラーを返す
        elif 'user' not in request.data:
            return Response({'error': 'User is required.'}, status=400)
        #ユーザーIDが存在しない場合、エラーを返す
        elif not YUser.objects.filter(pk=request.data['user']).exists():
            return Response({'error': 'User does not exist.'}, status=400)
        #ツイートIDが被っている場合、エラーを返す
        elif 'id' in request.data and Tweet.objects.filter(pk=request.data['id']).exists():
            return Response({'error': 'ID is incorrect.'}, status=400)
        #ツイートIDがない場合、ツイートIDを返す
        elif 'id' not in request.data:
            request.data['id'] = Tweet.objects.all().count() + 1
            while Tweet.objects.filter(pk=request.data['id']).exists():
                request.data['id'] += 1
        return super(TweetViewSet, self).create(request, *args, **kwargs)
        
    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user', None)

        #ユーザーIDが存在しない場合、ツイートを全て返す
        if user_id:
            queryset = Tweet.objects.filter(user_id=user_id)
        #ユーザーIDが存在する場合、ユーザーIDに紐づくツイートを返す
        else:
            queryset = Tweet.objects.all()

        serializer = TweetSerializer(queryset, many=True)
        return Response(serializer.data)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def create(self, request, *args, **kwargs):
        #フォロワーがない場合、エラーを返す
        if 'follower' not in request.data:
            return Response({'error': 'Follower is required.'}, status=400)
        #フォローされている人がない場合、エラーを返す
        elif 'following' not in request.data:
            return Response({'error': 'Following is required.'}, status=400)
        #フォロワーが存在しない場合、エラーを返す
        elif not YUser.objects.filter(pk=request.data['follower']).exists():
            return Response({'error': 'Follower does not exist.'}, status=400)
        #フォローされている人が存在しない場合、エラーを返す
        elif not YUser.objects.filter(pk=request.data['following']).exists():
            return Response({'error': 'Following does not exist.'}, status=400)
        #フォロワーとフォローされている人が同じ場合、エラーを返す
        elif request.data['follower'] == request.data['following']:
            return Response({'error': 'You cannot follow yourself.'}, status=400)
        #フォローされている人が既にフォロワーになっている場合、エラーを返す
        elif Follow.objects.filter(follower_id=request.data['follower'], following_id=request.data['following']).exists():
            return Response({'error': 'You are already following this user.'}, status=400)
        #フォローIDが被っている場合、フォローIDを返す
        else:
            if 'id' not in request.data:
                request.data['id'] = Follow.objects.all().count() + 1
                while Follow.objects.filter(pk=request.data['id']).exists():
                    request.data['id'] += 1
            return super(FollowViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        follower_id = request.query_params.get('follower', None)
        following_id = request.query_params.get('following', None)

        #フォロワーIDが存在しない場合、フォローされている人を全て返す
        if follower_id == following_id and not (follower_id is None and following_id is None):
            return Response({'error': 'You cannot follow yourself.'}, status=400)
        #フォローされている人IDが存在しない場合、フォロワーを全て返す
        elif follower_id and not following_id:
            queryset = Follow.objects.filter(follower_id=follower_id)
        #フォロワーIDが存在しない場合、フォローされている人を全て返す
        elif following_id and not follower_id:
            queryset = Follow.objects.filter(following_id=following_id)
        #フォロワーIDとフォローされている人IDが存在する場合、フォローを全て返す
        elif follower_id and following_id:
            queryset = Follow.objects.filter(follower_id=follower_id, following_id=following_id)
        #フォロワーIDとフォローされている人IDが存在しない場合、フォローを全て返す
        else:
            queryset = Follow.objects.all()
        
        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data)

    
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    lookup_field = 'to_user'

    def list(self, request, *args, **kwargs):
        from_user_id = request.query_params.get('from_user', None)
        to_user_id = request.query_params.get('to_user', None)
        tweet_id = request.query_params.get('tweet', None)

        #ユーザーIDが存在しない場合、通知を全て返す
        if not from_user_id and not to_user_id and not tweet_id:
            queryset = Notification.objects.all()
        elif tweet_id:
            if from_user_id and to_user_id:
                queryset = Notification.objects.filter(tweet_id=tweet_id, to_user_id=to_user_id, from_user_id=from_user_id)
            elif from_user_id and not to_user_id:
                queryset = Notification.objects.filter(tweet_id=tweet_id, from_user_id=from_user_id)
            elif to_user_id and not from_user_id:
                queryset = Notification.objects.filter(tweet_id=tweet_id, to_user_id=to_user_id)
            else:
                queryset = Notification.objects.filter(tweet_id=tweet_id)
        #ユーザーIDが存在する場合、ユーザーIDに紐づく通知を返す
        elif from_user_id and to_user_id:
            queryset = Notification.objects.filter(to_user_id=to_user_id, from_user_id=from_user_id)
        #ユーザーIDが存在する場合、ユーザーIDに紐づく通知を返す
        elif from_user_id and not to_user_id:
            queryset = Notification.objects.filter(from_user_id=from_user_id)
        #ユーザーIDが存在する場合、ユーザーIDに紐づく通知を返す
        elif to_user_id and not from_user_id:
            queryset = Notification.objects.filter(to_user_id=to_user_id)

        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)
