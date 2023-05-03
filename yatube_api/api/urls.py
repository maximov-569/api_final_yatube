from django.urls import path, include
from rest_framework import routers

from .views import CommentViewSet, PostViewSet, GroupViewSet, FollowViewSet

router = routers.DefaultRouter()
router.register(r'posts/(?P<post_id>[\d]+)/comments',
                CommentViewSet,
                basename='comments'
                )
router.register(r'posts', PostViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'follow', FollowViewSet)


urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
