import os
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')
os.system('python manage.py loaddata main/fixtures/initial_data.json')
# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Tweet, YUser, Follow, Notification
from .serializers import TweetSerializer, YUserSerializer, FollowSerializer, NotificationSerializer

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile


# 画像を読み込む関数
def load_pic(path):
    extension = os.path.splitext(path)[-1].lower() # 拡張子を小文字にして確実にマッチさせます
    if extension == '.png':
        name = 'test.png'
        content_type = 'image/png'
    elif extension == '.jpeg' or extension == '.jpg': # JPEGファイルの場合、'.jpeg'または'.jpg'を考慮
        name = 'test.jpeg'
        content_type = 'image/jpeg'
    else:
        name = None
        content_type = None

    return SimpleUploadedFile(name=name, content=open(path, 'rb').read(), content_type=content_type) if name and content_type else None


class UserCreateTestCase(APITestCase):
    '''
    ユーザー作成のテスト
    '''

    # -> テストコード ##########################################################
    # ユーザー作成のテスト
    def test_create_user(self):
        data = {
            'username': 'testuser',
            'password': 'testpass',
            'id': 1,
            'email': 'test@gmail.com'
        }
        self.check_is_valid(YUserSerializer, data=data, success=True)
        self.post(orgurl='yuser-list', data=data, success=status.HTTP_201_CREATED)

    # ユーザー作成のテスト(ユーザーネームがない場合)
    def test_create_user_without_username(self):
        data = {
            'password': 'testpass',
            'id': 1,
            'email': 'test@gmail.com',
        }
        self.check_is_valid(YUserSerializer, data=data, success=False)
        self.post(orgurl='yuser-list', data=data, success=status.HTTP_400_BAD_REQUEST)
        
    # ユーザー作成のテスト(パスワードがない場合)
    def test_create_tweet(self):
        self.create_user(1)
        data = {
            'content': 'test tweet',
            'user': 1,
            'id': 1,
        }
        self.check_is_valid(TweetSerializer, data=data, success=True)
        self.post(orgurl='tweet-list', data=data, success=status.HTTP_201_CREATED)
    
    # ユーザー作成のテスト(ユーザーネームが被っている場合)
    def test_create_tweet_without_content(self):
        self.create_user(1)
        data = {
            'user': 1,
            'id': 1
        }
        self.check_is_valid(TweetSerializer, data=data, success=False)
        self.post(orgurl='tweet-list', data=data, success=status.HTTP_400_BAD_REQUEST)

    # ユーザー作成のテスト(emailがない場合)
    def test_create_user_without_email(self):
        data = {
            'username': 'testuser',
            'password': 'testpass',
        }
        self.post(orgurl='yuser-list', data=data, success=status.HTTP_400_BAD_REQUEST)
        data['email'] = 'hogehoge@gmail.com'
        self.post(orgurl='yuser-list', data=data, success=status.HTTP_201_CREATED)
    
    # ユーザー作成のテスト(ユーザーIDがない場合)
    def test_create_user_with_profile(self):
        self.create_user(1)
        data = {
            'id': 1,
            'username': 'testuser1',
            'password': 'testpass1',
            'bio': 'test bio created',
            'pic': load_pic('main/tests/cat1.png')
        }
        if self.is_user_exists(1):
            self.put(orgurl=f'yuser-detail', kwargs=dict(pk=1), data=data, success=status.HTTP_200_OK)
        else:
            self.post(orgurl='yuser-list', data=data, success=status.HTTP_201_CREATED, format='multipart')

    # フォロー作成のテスト
    def test_create_follow(self):
        self.create_user(1)
        self.create_user(2)

        data = {
            'id': 1,
            'follower': 1,
            'following': 2,
            'followed_on': '2021-01-01T00:00:00Z'
        }
        self.check_is_valid(FollowSerializer, data=data, success=True)
        self.post(orgurl='follow-list', data=data, success=status.HTTP_201_CREATED)
    
    # フォロー作成のテスト(フォロワーがない場合)
    def test_create_follow_without_follower(self):
        self.create_user(2)
        data = {
            'id': 1,
            'following': 2,
            'followed_on': '2021-01-01T00:00:00Z'
        }
        self.check_is_valid(FollowSerializer, data=data, success=False)
        self.post(orgurl='follow-list', data=data, success=status.HTTP_400_BAD_REQUEST)
    
    # フォロー作成のテスト(フォローとフォロワーが同じ場合)
    def test_create_follow_with_same_follower_and_following(self):
        self.create_user(1)
        data = {
            'id': 1,
            'follower': 1,
            'following': 1,
        }
        self.check_is_valid(FollowSerializer, data=data, success=False)
        self.post(orgurl='follow-list', data=data, success=status.HTTP_400_BAD_REQUEST)

    # 通知作成のテスト
    def test_create_notification(self):
        self.create_user(1)
        self.create_user(2)
        self.create_tweet(id=1, user_id=2)
        data = {
            'to_user': 1,
            'from_user': 2,
            'tweet': 1,
            'notif_type': 'LIKE',
        }
        self.check_is_valid(NotificationSerializer, data=data, success=True)
        self.post(orgurl='notification-list', data=data, success=status.HTTP_201_CREATED)
    
    # 通知作成のテスト(送信元ユーザーがない場合)
    def test_create_notification_without_to_user(self):
        self.create_user(1)
        self.create_user(2)
        self.create_tweet(id=1, user_id=2)
        data = {
            'from_user': 2,
            'tweet': 1,
            'notif_type': 'LIKE',
        }
        self.check_is_valid(NotificationSerializer, data=data, success=False)
        self.post(orgurl='notification-list', data=data, success=status.HTTP_400_BAD_REQUEST)
    
    # ユーザー取得のテスト
    def test_get_user(self):
        self.create_user_with_profile(1)
        responce = self.get(orgurl='yuser-detail', kwargs=dict(pk=1), success=status.HTTP_200_OK)
        self.assertEqual(responce.data['username'], 'testuser1')
        self.assertEqual(responce.data['bio'], 'test bio created')

    # ツイート取得のテスト
    def test_get_tweet(self):
        self.create_tweet(id=1, user_id=1)
        self.create_tweet(id=2, user_id=1)
        self.create_tweet(id=3, user_id=1)
        self.create_tweet(id=4, user_id=2)
        url = reverse('tweet-list') + '?user=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    # フォロー取得のテスト
    def test_get_follow(self):
        self.create_follow(follower_id=1, following_id=2, id=1)
        self.create_follow(follower_id=1, following_id=3, id=2)
        self.create_follow(follower_id=1, following_id=4, id=3)
        self.create_follow(follower_id=3, following_id=2, id=4)
        url = reverse('follow-list') + '?follower=1'
        response = self.client.get(url, data={'follower': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.client.get(url).data), 3)

    # 通知取得のテスト
    def test_get_notification(self):
        self.create_notification(to_user_id=1, from_user_id=2, tweet_id=1, id=1)
        self.create_notification(to_user_id=1, from_user_id=2, tweet_id=2, id=2)
        self.create_notification(to_user_id=1, from_user_id=3, tweet_id=3, id=3)
        self.create_notification(to_user_id=2, from_user_id=4, tweet_id=4, id=4)

        url = reverse('notification-list') + '?to_user=1'
        response = self.client.get(url, data={'to_user': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.client.get(url).data), 3)

        url = reverse('notification-list') + '?from_user=2'
        response = self.client.get(url, data={'from_user': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.client.get(url).data), 2)

        url = reverse('notification-list') + '?to_user=1&from_user=2'
        response = self.client.get(url, data={'to_user': 1, 'from_user': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.client.get(url).data), 2)
        
        url = reverse('notification-list') + '?tweet=1'
        response = self.client.get(url, data={'tweet': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.client.get(url).data), 1)

    # idなしでオブジェクトを作成するテスト
    def test_create_objects_without_id(self):
        data = {
            'username': 'testuser',
            'password': 'testpass',
            'email': 'hogehoge@gmail.com'
        }
        self.post(orgurl='yuser-list', data=data, success=status.HTTP_201_CREATED)
        data = {
            'content': 'test tweet',
            'user': 1,
        }
        self.post(orgurl='tweet-list', data=data, success=status.HTTP_201_CREATED)
        self.create_user(2)
        data = {
            'follower': 1,
            'following': 2,
        }
        self.post(orgurl='follow-list', data=data, success=status.HTTP_201_CREATED)
    
    # idありでオブジェクトを作成するテスト
    def test_create_objects_with_same_id(self):
        data = {
            'username': 'testuser1',
            'password': 'testpass',
            'email': 'test@gmail.com',
            'id': 1,
        }
        self.post(orgurl='yuser-list', data=data, success=status.HTTP_201_CREATED)
        data = {
            'username': 'testuser2',
            'password': 'testpass',
            'email': 'test@gmail.com',
            'id': 1,
        }
        self.post(orgurl='yuser-list', data=data, success=status.HTTP_400_BAD_REQUEST)
        self.put(orgurl=f'yuser-detail', kwargs=dict(pk=1), data=data, success=status.HTTP_200_OK)
        data = {
            'content': 'test tweet',
            'user': 1,
            'id': 1,
        }
        self.post(orgurl='tweet-list', data=data, success=status.HTTP_201_CREATED)
        self.post(orgurl='tweet-list', data=data, success=status.HTTP_400_BAD_REQUEST)
        self.put(orgurl=f'tweet-detail', kwargs=dict(pk=1), data=data, success=status.HTTP_200_OK)
        self.create_user(2)
        data = {
            'follower': 1,
            'following': 2,
            'id': 1,
        }
        self.post(orgurl='follow-list', data=data, success=status.HTTP_201_CREATED)
        self.post(orgurl='follow-list', data=data, success=status.HTTP_400_BAD_REQUEST)
        self.put(orgurl='follow-detail', kwargs=dict(pk=1), data=data, success=status.HTTP_200_OK)


    # -> テストコード以外 ##########################################################
    # ユーザーが存在するかどうかを返す関数
    def is_user_exists(self, id=1):
        return YUser.objects.filter(pk=id).exists()
    
    def is_username_exists(self, username='testuser'):
        return YUser.objects.filter(username=username).exists()
    
    def is_email_exists(self, email='test@gmail.com'):
        return YUser.objects.filter(email=email).exists()

    # ツイートが存在するかどうかを返す関数
    def is_tweet_exists(self, id=1):
        return Tweet.objects.filter(pk=id).exists()
    
    # フォローが存在するかどうかを返す関数
    def is_follow_exists(self, id=1):
        return Follow.objects.filter(pk=id).exists()
    
    # 通知が存在するかどうかを返す関数
    def is_notification_exists(self, id=1):
        return Notification.objects.filter(pk=id).exists()
    
    # テスト用の通知を作成する関数
    def create_notification(self, to_user_id:int, from_user_id:int, tweet_id:int, id:int, verbose=False, assertioncheck=True):
        self.create_user(to_user_id)
        self.create_user(from_user_id)
        self.create_tweet(id=tweet_id, user_id=from_user_id)
        data = {
            'to_user': to_user_id,
            'from_user': from_user_id,
            'tweet': tweet_id,
            'id': id,
            'notif_type': 'LIKE'
        }
        self.check_is_valid(NotificationSerializer, data=data, success=True, verbose=verbose, assertioncheck=assertioncheck)
        self.post(orgurl='notification-list', data=data, success=status.HTTP_201_CREATED)
    
    # テスト用のフォローを作成する関数
    def create_follow(self, follower_id:int, following_id:int, id:int, verbose=False, assertioncheck=True):
        self.create_user(follower_id)
        self.create_user(following_id)
        data = {
            'follower': follower_id,
            'following': following_id,
            'followed_on': '2021-01-01T00:00:00Z',
            'id': id,
        }
        self.check_is_valid(FollowSerializer, data=data, success=True, verbose=verbose, assertioncheck=assertioncheck)
        if self.is_follow_exists(id):
            self.put(orgurl=f'follow-detail', kwargs=dict(pk=id), data=data, success=status.HTTP_200_OK)
        else:
            self.post(orgurl='follow-list', data=data, success=status.HTTP_201_CREATED)
    
    # テスト用のツイートを作成する関数
    def create_tweet(self, id:int, user_id:int, verbose=False, assertioncheck=True):
        self.create_user(user_id)
        data = {
            'content': f'test tweet{id}',
            'user': user_id,
            'id': id
        }
        self.check_is_valid(TweetSerializer, data=data, success=True, verbose=verbose, assertioncheck=assertioncheck)
        if self.is_tweet_exists(id):
            self.put(orgurl=f'tweet-detail', kwargs=dict(pk=id), data=data, success=status.HTTP_200_OK)
        else:
            self.post(orgurl='tweet-list', data=data, success=status.HTTP_201_CREATED)
    
    # テスト用のユーザーを作成する関数
    def create_user(self, id:int, verbose=False, assertioncheck=False):
        data = {
            'username': f'testuser{id}',
            'password': f'testpass{id}',
            'id': id,
            'email': f'test{id}@gamil.com',
        }
        self.check_is_valid(YUserSerializer, data=data, success=True, verbose=verbose, assertioncheck=assertioncheck)
        if self.is_username_exists(data['username']):
            while self.is_username_exists(data['username']):
                data['username'] += str(id)
        if self.is_email_exists(data['email']):
            while self.is_email_exists(data['email']):
                data['email'] += str(id)
        if not self.is_user_exists(id):
            self.post(orgurl='yuser-list', data=data, success=status.HTTP_201_CREATED)
        else:
            self.put(orgurl=f'yuser-detail', kwargs=dict(pk=id), data=data, success=status.HTTP_200_OK)
    
    # テスト用のユーザーを作成する関数(プロフィール付き)
    def create_user_with_profile(self, id:int, verbose=False, assertioncheck=False):
        data = {
            'username': f'testuser{id}',
            'password': f'testpass{id}',
            'id': id,
            'email': f'test@gamil.com',
            'bio': 'test bio created',
            'pic': load_pic('main/tests/cat1.png')
        }
        self.check_is_valid(YUserSerializer, data=data, success=True, verbose=verbose, assertioncheck=False)
        if self.is_user_exists(id):
            self.put(orgurl=f'yuser-detail', kwargs=dict(pk=id), data=data, success=status.HTTP_200_OK)
        else:
            self.post(orgurl='yuser-list', data=data, success=status.HTTP_201_CREATED, format='multipart')
    
    # データが正しいかどうかを返す関数
    def check_is_valid(self, serializer, data:dict, success=True, verbose=False, assertioncheck=True):
        ser = serializer(data=data)
        ser.is_valid()
        if verbose:
            print(ser.errors)
        if success and assertioncheck:
            self.assertEqual(ser.errors, {})
        elif not success and assertioncheck:
            self.assertNotEqual(ser.errors, {})
        else:
            pass
    
    # postメソッドを実行する関数
    def post(self, orgurl:str, data:dict, format='json', success=status.HTTP_201_CREATED):
        url = reverse(orgurl)
        response = self.client.post(path=url, data=data, format=format)
        self.assertEqual(response.status_code, success)

    # getメソッドを実行する関数
    def get(self, orgurl:str, kwargs:dict, success=status.HTTP_200_OK):
        url = reverse(orgurl, kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, success)
        return response
    
    # putメソッドを実行する関数
    def put(self, orgurl:str, kwargs:dict, data:dict, success=status.HTTP_200_OK):
        url = reverse(orgurl, kwargs=kwargs)
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, success)
    