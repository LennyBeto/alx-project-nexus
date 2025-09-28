# feed/api_views.py
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from django.db.models import Q, Prefetch
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import Post, Comment, Like, Share, Follow, UserProfile
from .serializers import (
    PostSerializer, CommentSerializer, UserSerializer, 
    UserProfileSerializer, LikeSerializer, ShareSerializer, 
    FollowSerializer, PostCreateSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(
    summary="API Health Check",
    description="Check if the API is running and healthy",
    responses={200: {"description": "API is healthy"}}
)
@api_view(['GET'])
@permission_classes([])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'Social Media Feed API is running',
        'version': '1.0.0'
    })


@extend_schema(
    summary="API Information",
    description="Get API information and available endpoints",
    responses={200: {"description": "API information"}}
)
@api_view(['GET'])
@permission_classes([])
def api_info(request):
    """API information endpoint"""
    return Response({
        'name': 'Social Media Feed API',
        'version': '1.0.0',
        'description': 'A scalable GraphQL and REST API for social media applications',
        'endpoints': {
            'graphql': '/graphql/',
            'rest_api': '/api/',
            'admin': '/admin/',
            'docs': '/api/docs/',
            'redoc': '/api/redoc/'
        },
        'features': [
            'GraphQL API with mutations and queries',
            'REST API with full CRUD operations',
            'User authentication and profiles',
            'Post creation, editing, and deletion',
            'Like and comment system',
            'Follow/unfollow functionality',
            'Real-time interactions',
            'Optimized database queries'
        ]
    })


class PostListCreateView(generics.ListCreateAPIView):
    """List all posts or create a new post"""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = Post.objects.filter(is_deleted=False).select_related(
            'author', 'author__profile'
        ).prefetch_related(
            Prefetch('comments', queryset=Comment.objects.filter(is_deleted=False))
        ).order_by('-created_at')
        
        # Filter by author
        author_id = self.request.query_params.get('author_id')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(content__icontains=search) | 
                Q(author__username__icontains=search)
            )
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        summary="List Posts",
        description="Get a paginated list of posts with optional filtering",
        parameters=[
            OpenApiParameter("author_id", OpenApiTypes.INT, description="Filter by author ID"),
            OpenApiParameter("search", OpenApiTypes.STR, description="Search in content and author username"),
            OpenApiParameter("page", OpenApiTypes.INT, description="Page number"),
            OpenApiParameter("page_size", OpenApiTypes.INT, description="Number of items per page"),
        ],
        examples=[
            OpenApiExample(
                "Basic request",
                description="Get first page of posts",
                value={"page": 1, "page_size": 20}
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create Post",
        description="Create a new post (authentication required)",
        request=PostCreateSerializer,
        responses={201: PostSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a post"""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Post.objects.filter(is_deleted=False).select_related(
            'author', 'author__profile'
        ).prefetch_related(
            Prefetch('comments', queryset=Comment.objects.filter(is_deleted=False).select_related('author'))
        )
    
    def get_object(self):
        obj = super().get_object()
        # Check if user owns the post for update/delete operations
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.author != self.request.user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You don't have permission to modify this post")
        return obj
    
    def perform_destroy(self, instance):
        # Soft delete
        instance.delete()

    @extend_schema(
        summary="Get Post",
        description="Retrieve a single post by ID",
        responses={200: PostSerializer, 404: {"description": "Post not found"}}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update Post",
        description="Update a post (only by the author)",
        request=PostCreateSerializer,
        responses={200: PostSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Delete Post",
        description="Delete a post (only by the author)",
        responses={204: {"description": "Post deleted successfully"}}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class UserFeedView(generics.ListAPIView):
    """Get personalized user feed"""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        user = self.request.user
        # Get posts from followed users
        following_ids = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
        
        queryset = Post.objects.filter(
            author_id__in=following_ids,
            is_deleted=False
        ).select_related(
            'author', 'author__profile'
        ).order_by('-created_at')
        
        # If no following, show trending posts
        if not queryset.exists():
            queryset = Post.objects.filter(is_deleted=False).select_related(
                'author', 'author__profile'
            ).order_by('-likes_count', '-created_at')[:50]
        
        return queryset

    @extend_schema(
        summary="User Feed",
        description="Get personalized feed based on followed users",
        responses={200: PostSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TrendingPostsView(generics.ListAPIView):
    """Get trending posts"""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Post.objects.filter(is_deleted=False).select_related(
            'author', 'author__profile'
        ).order_by('-likes_count', '-comments_count', '-created_at')[:50]

    @extend_schema(
        summary="Trending Posts",
        description="Get posts ordered by popularity (likes and comments)",
        responses={200: PostSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@extend_schema(
    summary="Like/Unlike Post",
    description="Toggle like status for a post",
    request=None,
    responses={
        200: {"description": "Like toggled successfully", "example": {"message": "Post liked", "is_liked": True}},
        404: {"description": "Post not found"}
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    """Like or unlike a post"""
    try:
        post = Post.objects.get(id=post_id, is_deleted=False)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
        return Response({
            'message': 'Post unliked',
            'is_liked': False,
            'likes_count': post.likes_count
        })
    
    return Response({
        'message': 'Post liked',
        'is_liked': True,
        'likes_count': post.likes_count
    })


class CommentListCreateView(generics.ListCreateAPIView):
    """List comments for a post or create a new comment"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(
            post_id=post_id,
            parent__isnull=True,  # Top-level comments only
            is_deleted=False
        ).select_related('author', 'author__profile').prefetch_related(
            Prefetch('replies', queryset=Comment.objects.filter(is_deleted=False).select_related('author'))
        ).order_by('-created_at')
    
    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        try:
            post = Post.objects.get(id=post_id, is_deleted=False)
        except Post.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Post not found")
        
        serializer.save(author=self.request.user, post=post)

    @extend_schema(
        summary="List Comments",
        description="Get comments for a specific post",
        responses={200: CommentSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create Comment",
        description="Create a new comment on a post",
        responses={201: CommentSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(
    summary="Follow/Unfollow User",
    description="Toggle follow status for a user",
    responses={
        200: {"description": "Follow status toggled", "example": {"message": "Now following user", "is_following": True}},
        404: {"description": "User not found"}
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """Follow or unfollow a user"""
    if request.user.id == user_id:
        return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    follow, created = Follow.objects.get_or_create(
        follower=request.user, 
        following=target_user
    )
    
    if not created:
        follow.delete()
        return Response({
            'message': f'Unfollowed {target_user.username}',
            'is_following': False
        })
    
    return Response({
        'message': f'Now following {target_user.username}',
        'is_following': True
    })


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get or update user profile"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self):
        user_id = self.kwargs.get('user_id', self.request.user.id)
        profile, created = UserProfile.objects.get_or_create(
            user_id=user_id,
            defaults={'user_id': user_id}
        )
        return profile

    @extend_schema(
        summary="Get User Profile",
        description="Retrieve user profile information",
        responses={200: UserProfileSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update Profile",
        description="Update user profile (only own profile)",
        responses={200: UserProfileSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class UserListView(generics.ListAPIView):
    """List users with search functionality"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        queryset = User.objects.select_related('profile').order_by('-date_joined')
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) | 
                Q(first_name__icontains=search) | 
                Q(last_name__icontains=search)
            )
        
        return queryset

    @extend_schema(
        summary="List Users",
        description="Get a list of users with optional search",
        parameters=[
            OpenApiParameter("search", OpenApiTypes.STR, description="Search in username and name"),
        ],
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
