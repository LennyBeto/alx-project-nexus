# feed/queries.py
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth.models import User
from django.db.models import Q, Prefetch
from .models import Post, Comment, Like, Share, Follow
from .types import UserType, PostType, CommentType, LikeType, ShareType, FollowType

class Query(graphene.ObjectType): 
    # User queries
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int(), username=graphene.String())
    me = graphene.Field(UserType)
    
    # Post queries
    posts = graphene.List(
        PostType,
        limit=graphene.Int(default_value=20),
        offset=graphene.Int(default_value=0),
        author_id=graphene.Int(),
        search=graphene.String()
    )
    post = graphene.Field(PostType, id=graphene.Int(required=True))
    feed = graphene.List(
        PostType,
        limit=graphene.Int(default_value=20),
        offset=graphene.Int(default_value=0)
    )
    
    # Comment queries
    comments = graphene.List(
        CommentType,
        post_id=graphene.Int(required=True),
        limit=graphene.Int(default_value=50),
        offset=graphene.Int(default_value=0)
    )
    comment = graphene.Field(CommentType, id=graphene.Int(required=True))
    
    # Interaction queries
    post_likes = graphene.List(LikeType, post_id=graphene.Int(required=True))
    post_shares = graphene.List(ShareType, post_id=graphene.Int(required=True))
    user_followers = graphene.List(FollowType, user_id=graphene.Int(required=True))
    user_following = graphene.List(FollowType, user_id=graphene.Int(required=True))
    
    def resolve_users(self, info):
        return User.objects.all()
    
    def resolve_user(self, info, id=None, username=None):
        if id:
            try:
                return User.objects.get(pk=id)
            except User.DoesNotExist:
                return None
        if username:
            try:
                return User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        return None
    
    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None
    
    def resolve_posts(self, info, limit=20, offset=0, author_id=None, search=None):
        queryset = Post.objects.select_related('author').prefetch_related(
            'likes', 'comments', 'shares'
        )
        
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        if search:
            queryset = queryset.filter(
                Q(content__icontains=search) | Q(author__username__icontains=search)
            )
        
        return queryset[offset:offset + limit]
    
    def resolve_post(self, info, id):
        try:
            return Post.objects.select_related('author').prefetch_related(
                'likes', 'comments', 'shares'
            ).get(pk=id)
        except Post.DoesNotExist:
            return None
    
    def resolve_feed(self, info, limit=20, offset=0):
        user = info.context.user
        if not user.is_authenticated:
            # Return public feed for anonymous users
            return Post.objects.select_related('author').prefetch_related(
                'likes', 'comments', 'shares'
            )[:limit]
        
        # Get posts from followed users
        following_users = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
        
        queryset = Post.objects.select_related('author').prefetch_related(
            'likes', 'comments', 'shares'
        ).filter(
            Q(author__in=following_users) | Q(author=user)
        ).distinct()
        
        return queryset[offset:offset + limit]
    
    def resolve_comments(self, info, post_id, limit=50, offset=0):
        return Comment.objects.select_related('author', 'post').prefetch_related(
            'replies', 'likes'
        ).filter(post_id=post_id, parent__isnull=True)[offset:offset + limit]
    
    def resolve_comment(self, info, id):
        try:
            return Comment.objects.select_related('author', 'post').prefetch_related(
                'replies', 'likes'
            ).get(pk=id)
        except Comment.DoesNotExist:
            return None
    
    def resolve_post_likes(self, info, post_id):
        return Like.objects.select_related('user').filter(post_id=post_id)
    
    def resolve_post_shares(self, info, post_id):
        return Share.objects.select_related('user').filter(post_id=post_id)
    
    def resolve_user_followers(self, info, user_id):
        return Follow.objects.select_related('follower').filter(following_id=user_id)
    
    def resolve_user_following(self, info, user_id):
        return Follow.objects.select_related('following').filter(follower_id=user_id)

