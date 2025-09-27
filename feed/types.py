import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Share, Follow

class UserType(DjangoObjectType):
    full_name = graphene.String()
    followers_count = graphene.Int()
    following_count = graphene.Int()
    posts_count = graphene.Int()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
    
    def resolve_full_name(self, info):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def resolve_followers_count(self, info):
        return self.followers.count()
    
    def resolve_following_count(self, info):
        return self.following.count()
    
    def resolve_posts_count(self, info):
        return self.posts.count()

class PostType(DjangoObjectType):
    is_liked_by_user = graphene.Boolean()
    is_shared_by_user = graphene.Boolean()
    
    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'image_url', 'created_at', 'updated_at', 
                 'likes_count', 'comments_count', 'shares_count')
    
    def resolve_is_liked_by_user(self, info):
        user = info.context.user
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False
    
    def resolve_is_shared_by_user(self, info):
        user = info.context.user
        if user.is_authenticated:
            return self.shares.filter(user=user).exists()
        return False

class CommentType(DjangoObjectType):
    replies_count = graphene.Int()
    is_liked_by_user = graphene.Boolean()
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_at', 'updated_at', 'parent')
    
    def resolve_replies_count(self, info):
        return self.replies.count()
    
    def resolve_is_liked_by_user(self, info):
        user = info.context.user
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False

class LikeType(DjangoObjectType):
    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'comment', 'like_type', 'created_at')

class ShareType(DjangoObjectType):
    class Meta:
        model = Share
        fields = ('id', 'user', 'post', 'message', 'created_at')

class FollowType(DjangoObjectType):
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'created_at')
