
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TweetViewSet, YUserViewSet, FollowViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'users', YUserViewSet)
router.register(r'tweets', TweetViewSet)
router.register(r'follows', FollowViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
