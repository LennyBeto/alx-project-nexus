# feed/urls.py
from django.urls import path
from .api_views import (
    PostListCreateView, PostDetailView, UserFeedView, TrendingPostsView,
    CommentListCreateView, UserProfileView, UserListView,
    like_post, follow_user
)

app_name = 'feed'

urlpatterns = [
    # Posts
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/like/', like_post, name='like-post'),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='post-comments'),
    
    # Feed
    path('feed/', UserFeedView.as_view(), name='user-feed'),
    path('trending/', TrendingPostsView.as_view(), name='trending-posts'),
    
    # Users
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/follow/', follow_user, name='follow-user'),
    path('users/<int:user_id>/profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/', UserProfileView.as_view(), name='my-profile'),
]