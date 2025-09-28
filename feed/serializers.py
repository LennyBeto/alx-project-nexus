# feed/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Share, Follow, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    full_name = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'full_name', 'date_joined', 'followers_count', 
            'following_count', 'posts_count'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username
    
    def get_followers_count(self, obj):
        return getattr(obj.profile, 'followers_count', 0) if hasattr(obj, 'profile') else 0
    
    def get_following_count(self, obj):
        return getattr(obj.profile, 'following_count', 0) if hasattr(obj, 'profile') else 0
    
    def get_posts_count(self, obj):
        return getattr(obj.profile, 'posts_count', 0) if hasattr(obj, 'profile') else 0


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'bio', 'location', 'birth_date', 'avatar',
            'followers_count', 'following_count', 'posts_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'followers_count', 'following_count', 'posts_count',
            'created_at', 'updated_at'
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'parent', 'content', 'likes_count',
            'replies_count', 'replies', 'is_liked_by_user', 
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'likes_count', 'replies_count', 
            'created_at', 'updated_at'
        ]
    
    def get_replies(self, obj):
        if hasattr(obj, 'replies'):
            replies = obj.replies.filter(is_deleted=False)[:5]  # Limit replies to avoid deep nesting
            return CommentSerializer(replies, many=True, context=self.context).data
        return []
    
    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post model"""
    author = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'content', 'image', 'likes_count',
            'comments_count', 'shares_count', 'comments',
            'is_liked_by_user', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'likes_count', 'comments_count',
            'shares_count', 'created_at', 'updated_at'
        ]
    
    def get_comments(self, obj):
        # Get top-level comments with limited depth to avoid performance issues
        if hasattr(obj, 'comments'):
            comments = obj.comments.filter(parent__isnull=True, is_deleted=False)[:3]
            return CommentSerializer(comments, many=True, context=self.context).data
        return []
    
    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating posts"""
    
    class Meta:
        model = Post
        fields = ['content', 'image']
    
    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Content cannot be empty")
        if len(value) > 2000:
            raise serializers.ValidationError("Content cannot exceed 2000 characters")
        return value.strip()


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for Like model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ShareSerializer(serializers.ModelSerializer):
    """Serializer for Share model"""
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    
    class Meta:
        model = Share
        fields = ['id', 'user', 'post', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'post', 'created_at']


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for Follow model"""
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)
    
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']
        read_only_fields = ['id', 'follower', 'following', 'created_at']


class UserStatsSerializer(serializers.Serializer):
    """Serializer for user statistics"""
    posts_count = serializers.IntegerField()
    followers_count = serializers.IntegerField()
    following_count = serializers.IntegerField()
    likes_received = serializers.IntegerField()
    comments_received = serializers.IntegerField()


class FeedStatsSerializer(serializers.Serializer):
    """Serializer for feed statistics"""
    total_posts = serializers.IntegerField()
    total_users = serializers.IntegerField()
    total_likes = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    posts_today = serializers.IntegerField()
    new_users_today = serializers.IntegerField()