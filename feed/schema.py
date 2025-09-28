#feed/schema.py
import graphene
from django.contrib.auth.models import User
from django.db.models import Q, Prefetch
from .models import Post, Comment, Like, Share, Follow, UserProfile
from .types import UserType, UserProfileType, PostType, CommentType, LikeType, ShareType, FollowType
from .mutations import Mutation


class Query(graphene.ObjectType):
    """GraphQL queries"""
    
    # Post queries
    posts = graphene.List(
        PostType,
        limit=graphene.Int(default_value=20),
        offset=graphene.Int(default_value=0),
        author_id=graphene.Int(),
        search=graphene.String()
    )
    post = graphene.Field(PostType, id=graphene.Int(required=True))
    
    # User queries
    users = graphene.List(UserType, limit=graphene.Int(default_value=20))
    user = graphene.Field(UserType, id=graphene.Int(), username=graphene.String())
    user_profile = graphene.Field(UserProfileType, user_id=graphene.Int())
    
    # Feed queries
    user_feed = graphene.List(PostType, limit=graphene.Int(default_value=20))
    trending_posts = graphene.List(PostType, limit=graphene.Int(default_value=10))
    
    # Comment queries
    post_comments = graphene.List(
        CommentType,
        post_id=graphene.Int(required=True),
        limit=graphene.Int(default_value=20)
    )
    
    # Follow queries
    user_followers = graphene.List(UserType, user_id=graphene.Int(required=True))
    user_following = graphene.List(UserType, user_id=graphene.Int(required=True))
    
    # Like queries
    post_likes = graphene.List(LikeType, post_id=graphene.Int(required=True))
    comment_likes = graphene.List(LikeType, comment_id=graphene.Int(required=True))
    
    # Share queries
    post_shares = graphene.List(ShareType, post_id=graphene.Int(required=True))

    def resolve_posts(self, info, limit=20, offset=0, author_id=None, search=None):
        """Resolve posts with filtering and pagination"""
        queryset = Post.objects.filter(is_deleted=False).select_related(
            'author', 'author__profile'
        ).prefetch_related(
            Prefetch('comments', queryset=Comment.objects.filter(is_deleted=False))
        ).order_by('-created_at')
        
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        if search:
            queryset = queryset.filter(
                Q(content__icontains=search) | 
                Q(author__username__icontains=search)
            )
        
        return queryset[offset:offset+limit]

    def resolve_post(self, info, id):
        """Resolve single post by ID"""
        try:
            return Post.objects.select_related(
                'author', 'author__profile'
            ).prefetch_related(
                Prefetch('comments', queryset=Comment.objects.filter(is_deleted=False).select_related('author'))
            ).get(id=id, is_deleted=False)
        except Post.DoesNotExist:
            return None

    def resolve_users(self, info, limit=20):
        """Resolve users list"""
        return User.objects.select_related('profile').order_by('-date_joined')[:limit]

    def resolve_user(self, info, id=None, username=None):
        """Resolve single user"""
        try:
            if id:
                return User.objects.select_related('profile').get(id=id)
            elif username:
                return User.objects.select_related('profile').get(username=username)
        except User.DoesNotExist:
            return None

    def resolve_user_profile(self, info, user_id):
        """Resolve user profile"""
        try:
            return UserProfile.objects.select_related('user').get(user_id=user_id)
        except UserProfile.DoesNotExist:
            return None

    def resolve_user_feed(self, info, limit=20):
        """Resolve personalized user feed"""
        user = info.context.user
        if not user.is_authenticated:
            # Return popular posts for anonymous users
            return Post.objects.filter(is_deleted=False).select_related(
                'author', 'author__profile'
            ).order_by('-likes_count', '-created_at')[:limit]
        
        # Get posts from followed users
        following_ids = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
        
        if following_ids:
            queryset = Post.objects.filter(
                author_id__in=following_ids,
                is_deleted=False
            ).select_related(
                'author', 'author__profile'
            ).order_by('-created_at')[:limit]
        else:
            # If user doesn't follow anyone, show trending posts
            queryset = Post.objects.filter(is_deleted=False).select_related(
                'author', 'author__profile'
            ).order_by('-likes_count', '-created_at')[:limit]
        
        return queryset

    def resolve_trending_posts(self, info, limit=10):
        """Resolve trending posts based on engagement"""
        return Post.objects.filter(is_deleted=False).select_related(
            'author', 'author__profile'
        ).order_by('-likes_count', '-comments_count', '-created_at')[:limit]

    def resolve_post_comments(self, info, post_id, limit=20):
        """Resolve comments for a post"""
        return Comment.objects.filter(
            post_id=post_id,
            parent__isnull=True,  # Top-level comments only
            is_deleted=False
        ).select_related('author', 'author__profile').prefetch_related(
            Prefetch('replies', queryset=Comment.objects.filter(is_deleted=False).select_related('author'))
        ).order_by('-created_at')[:limit]

    def resolve_user_followers(self, info, user_id):
        """Resolve user's followers"""
        return User.objects.filter(
            following__following_id=user_id
        ).select_related('profile').order_by('-date_joined')

    def resolve_user_following(self, info, user_id):
        """Resolve users that a user is following"""
        return User.objects.filter(
            followers__follower_id=user_id
        ).select_related('profile').order_by('-date_joined')

    def resolve_post_likes(self, info, post_id):
        """Resolve likes for a specific post"""
        return Like.objects.filter(
            post_id=post_id
        ).select_related('user', 'user__profile').order_by('-created_at')

    def resolve_comment_likes(self, info, comment_id):
        """Resolve likes for a specific comment"""
        return Like.objects.filter(
            comment_id=comment_id
        ).select_related('user', 'user__profile').order_by('-created_at')

    def resolve_post_shares(self, info, post_id):
        """Resolve shares for a specific post"""
        return Share.objects.filter(
            post_id=post_id
        ).select_related('user', 'user__profile', 'post').order_by('-created_at')


# Main schema combining queries and mutations
schema = graphene.Schema(query=Query, mutation=Mutation)