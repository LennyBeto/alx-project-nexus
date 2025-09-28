# feed/types.py
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Share, Follow, UserProfile


class UserType(DjangoObjectType):
    """GraphQL type for User model"""
    full_name = graphene.String()
    
    class Meta:
        model = User
        fields = '__all__'
    def resolve_full_name(self, info):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class UserProfileType(DjangoObjectType):
    """GraphQL type for UserProfile model"""
    full_name = graphene.String()
    
    class Meta:
        model = UserProfile
        fields = '__all__'
    
    def resolve_full_name(self, info):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username


class PostType(DjangoObjectType):
    """GraphQL type for Post model"""
    author = graphene.Field(UserType)
    is_liked_by_user = graphene.Boolean()
    
    class Meta:
        model = Post
        fields = '__all__'
    
    def resolve_is_liked_by_user(self, info):
        user = info.context.user
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False


class CommentType(DjangoObjectType):
    """GraphQL type for Comment model"""
    author = graphene.Field(UserType)
    replies = graphene.List(lambda: CommentType)
    is_liked_by_user = graphene.Boolean()
    
    class Meta:
        model = Comment
        fields = '__all__'
    
    def resolve_replies(self, info):
        return self.replies.filter(is_deleted=False).select_related('author')
    
    def resolve_is_liked_by_user(self, info):
        user = info.context.user
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False


class LikeType(DjangoObjectType):
    """GraphQL type for Like model"""
    class Meta:
        model = Like
        fields = '__all__'


class ShareType(DjangoObjectType):
    """GraphQL type for Share model"""
    class Meta:
        model = Share
        fields = '__all__'


class FollowType(DjangoObjectType):
    """GraphQL type for Follow model"""
    class Meta:
        model = Follow
        fields = '__all__'