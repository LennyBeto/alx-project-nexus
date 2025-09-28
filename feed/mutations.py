import graphene
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Post, Comment, Like, Share, Follow, UserProfile
# from .types import PostType, CommentType, ShareType, UserProfileType, UserType

class CreatePost(graphene.Mutation):
    """Mutation to create a new post"""
    class Arguments:
        content = graphene.String(required=True)
        image = graphene.String()  # Base64 encoded image or image URL

    success = graphene.Boolean()
    message = graphene.String()
    post = graphene.Field('feed.types.PostType')
    errors = graphene.List(graphene.String)

    def mutate(self, info, content, image=None):
        user = info.context.user
        if not user.is_authenticated:
            return CreatePost(
                success=False, 
                message="Authentication required",
                errors=["User must be authenticated to create posts"]
            )

        # Validate content
        if not content or not content.strip():
            return CreatePost(
                success=False, 
                message="Content cannot be empty",
                errors=["Post content is required"]
            )

        if len(content.strip()) > 2000:
            return CreatePost(
                success=False, 
                message="Content too long",
                errors=["Post content cannot exceed 2000 characters"]
            )

        try:
            with transaction.atomic():
                post = Post.objects.create(
                    author=user,
                    content=content.strip()
                )
                # Handle image if provided (extend for actual image processing)
                if image:
                    pass

                return CreatePost(
                    success=True, 
                    message="Post created successfully", 
                    post=post,
                    errors=[]
                )
        except Exception as e:
            return CreatePost(
                success=False, 
                message="Failed to create post",
                errors=[str(e)]
            )

class UpdatePost(graphene.Mutation):
    """Mutation to update an existing post"""
    class Arguments:
        post_id = graphene.Int(required=True)
        content = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    post = graphene.Field('feed.types.PostType')
    errors = graphene.List(graphene.String)

    def mutate(self, info, post_id, content):
        user = info.context.user
        if not user.is_authenticated:
            return UpdatePost(
                success=False, 
                message="Authentication required",
                errors=["User must be authenticated to update posts"]
            )

        try:
            post = Post.objects.get(id=post_id, author=user, is_deleted=False)
        except Post.DoesNotExist:
            return UpdatePost(
                success=False, 
                message="Post not found or access denied",
                errors=["Post does not exist or you don't have permission to edit it"]
            )

        # Validate content
        if not content or not content.strip():
            return UpdatePost(
                success=False, 
                message="Content cannot be empty",
                errors=["Post content is required"]
            )

        if len(content.strip()) > 2000:
            return UpdatePost(
                success=False, 
                message="Content too long",
                errors=["Post content cannot exceed 2000 characters"]
            )

        try:
            with transaction.atomic():
                post.content = content.strip()
                post.save()

                return UpdatePost(
                    success=True, 
                    message="Post updated successfully", 
                    post=post,
                    errors=[]
                )
        except Exception as e:
            return UpdatePost(
                success=False, 
                message="Failed to update post",
                errors=[str(e)]
            )

class DeletePost(graphene.Mutation):
    """Mutation to delete a post (soft delete)"""
    class Arguments:
        post_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    errors = graphene.List(graphene.String)

    def mutate(self, info, post_id):
        user = info.context.user
        if not user.is_authenticated:
            return DeletePost(
                success=False, 
                message="Authentication required",
                errors=["User must be authenticated to delete posts"]
            )

        try:
            post = Post.objects.get(id=post_id, author=user, is_deleted=False)
        except Post.DoesNotExist:
            return DeletePost(
                success=False, 
                message="Post not found or access denied",
                errors=["Post does not exist or you don't have permission to delete it"]
            )

        try:
            with transaction.atomic():
                post.delete()  # This is soft delete as implemented in the model
                return DeletePost(
                    success=True, 
                    message="Post deleted successfully",
                    errors=[]
                )
        except Exception as e:
            return DeletePost(
                success=False, 
                message="Failed to delete post",
                errors=[str(e)]
            )

class LikePost(graphene.Mutation):
    """Mutation to like/unlike a post"""
    class Arguments:
        post_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    is_liked = graphene.Boolean()
    likes_count = graphene.Int()
    errors = graphene.List(graphene.String)

    def mutate(self, info, post_id):
        user = info.context.user
        if not user.is_authenticated:
            return LikePost(
                success=False, 
                message="Authentication required",
                errors=["User must be authenticated to like posts"]
            )

        try:
            post = Post.objects.get(id=post_id, is_deleted=False)
        except Post.DoesNotExist:
            return LikePost(
                success=False, 
                message="Post not found",
                errors=["Post does not exist or has been deleted"]
            )

        try:
            with transaction.atomic():
                like, created = Like.objects.get_or_create(user=user, post=post)

                if not created:
                    # Unlike the post
                    like.delete()
                    post.refresh_from_db()  # Refresh to get updated likes_count
                    return LikePost(
                        success=True, 
                        message="Post unliked successfully", 
                        is_liked=False,
                        likes_count=post.likes_count,
                        errors=[]
                    )

                post.refresh_from_db()  # Refresh to get updated likes_count
                return LikePost(
                    success=True, 
                    message="Post liked successfully", 
                    is_liked=True,
                    likes_count=post.likes_count,
                    errors=[]
                )
        except Exception as e:
            return LikePost(
                success=False, 
                message="Failed to like/unlike post",
                errors=[str(e)]
            )

class CreateComment(graphene.Mutation):
    """Mutation to create a comment"""
    class Arguments:
        post_id = graphene.Int(required=True)
        content = graphene.String(required=True)
        parent_id = graphene.Int()

    success = graphene.Boolean()
    message = graphene.String()
    comment = graphene.Field('feed.types.CommentType')
    errors = graphene.List(graphene.String)

    def mutate(self, info, post_id, content, parent_id=None):
        user = info.context.user
        if not user.is_authenticated:
            return CreateComment(
                success=False, 
                message="Authentication required",
                errors=["User must be authenticated to comment"]
            )

        try:
            post = Post.objects.get(id=post_id, is_deleted=False)
        except Post.DoesNotExist:
            return CreateComment(
                success=False, 
                message="Post not found",
                errors=["Post does not exist or has been deleted"]
            )

        # Validate content
        if not content or not content.strip():
            return CreateComment(
                success=False, 
                message="Content cannot be empty",
                errors=["Comment content is required"]
            )

        if len(content.strip()) > 1000:
            return CreateComment(
                success=False, 
                message="Content too long",
                errors=["Comment content cannot exceed 1000 characters"]
            )

        # Check parent comment if provided
        parent = None
        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id, post=post, is_deleted=False)
            except Comment.DoesNotExist:
                return CreateComment(
                    success=False, 
                    message="Parent comment not found",
                    errors=["Parent comment does not exist or has been deleted"]
                )

        try:
            with transaction.atomic():
                comment = Comment.objects.create(
                    post=post,
                    author=user,
                    parent=parent,
                    content=content.strip()
                )

                return CreateComment(
                    success=True, 
                    message="Comment created successfully", 
                    comment=comment,
                    errors=[]
                )
        except Exception as e:
            return CreateComment(
                success=False, 
                message="Failed to create comment",
                errors=[str(e)]
            )

class UpdateComment(graphene.Mutation):
    """Mutation to update a comment"""
    class Arguments:
        comment_id = graphene.Int(required=True)
        content = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    comment = graphene.Field('feed.types.CommentType')
    errors = graphene.List(graphene.String)

    def mutate(self, info, comment_id, content):
        user = info.context.user
        if not user.is_authenticated:
            return UpdateComment(
                success=False, 
                message="Authentication required",
                errors=["User must be authenticated to update comments"]
            )

        try:
            comment = Comment.objects.get(id=comment_id, author=user, is_deleted=False)
        except Comment.DoesNotExist:
            return UpdateComment(
                success=False, 
                message="Comment not found or access denied",
                errors=["Comment does not exist or you don't have permission to edit it"]
            )

        # Validate content
        if not content or not content.strip():
            return UpdateComment(
                success=False, 
                message="Content cannot be empty",
                errors=["Comment content is required"]
            )

        if len(content.strip()) > 1000:
            return UpdateComment(
                success=False, 
                message="Content too long",
                errors=["Comment content cannot exceed 1000 characters"]
            )

        try:
            with transaction.atomic():
                comment.content = content.strip()
                comment.save()

                return UpdateComment(
                    success=True, 
                    message="Comment updated successfully", 
                    comment=comment,
                    errors=[]
                )
        except Exception as e:
            return UpdateComment(
                success=False, 
                message="Failed to update comment",
                errors=[str(e)]
            )

class DeleteComment(graphene.Mutation):
    """Mutation to delete a comment (soft delete)"""
    class Arguments:
        comment_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    errors = graphene.List(graphene.String)

    def mutate(self, info, comment_id):
        user = info.context.user
        if not user.is_authenticated:
            return DeleteComment(
                success=False, 
                message="Authentication required",
                errors=["User must be authenticated to delete comments"]
            )

        try:
            comment = Comment.objects.get(id=comment_id, author=user, is_deleted=False)
        except Comment.DoesNotExist:
            return DeleteComment(
                success=False, 
                message="Comment not found or access denied",
                errors=["Comment does not exist or you don't have permission to delete it"]
            )

        try:
            with transaction.atomic():
                comment.delete()  # This is soft delete as implemented in the model
                return DeleteComment(
                    success=True, 
                    message="Comment deleted successfully",
                    errors=[]
                )
        except Exception as e:
            return DeleteComment(
                success=False, 
                message="Failed to delete comment",
                errors=[str(e)]
            )

class LikeComment(graphene.Mutation):
    """Mutation to like/unlike a comment"""
    class Arguments:
        comment_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    is_liked = graphene.Boolean()
    likes_count = graphene.Int()
    errors = graphene.List(graphene.String)

    def mutate(self, info, comment_id):
        user = info.context.user
        if not user.is_authenticated:
            return LikeComment(
                success=False, 
                message="Authentication required",
                errors=["User must be authenticated to like comments"]
            )

        try:
            comment = Comment.objects.get(id=comment_id, is_deleted=False)
        except Comment.DoesNotExist:
            return LikeComment(
                success=False, 
                message="Comment not found",
                errors=["Comment does not exist or has been deleted"]
            )

        try:
            with transaction.atomic():
                like, created = Like.objects.get_or_create(user=user, comment=comment)

                if not created:
                    like.delete()
                    comment.refresh_from_db()  # Refresh to get updated likes_count
                    return LikeComment(
                        success=True, 
                        message="Comment unliked successfully", 
                        is_liked=False,
                        likes_count=comment.likes_count,
                        errors=[]
                    )

                comment.refresh_from_db()  # Refresh to get updated likes_count
                return LikeComment(
                    success=True, 
                    message="Comment liked successfully", 
                    is_liked=True,
                    likes_count=comment.likes_count,
                    errors=[]
                )
        except Exception as e:
            return LikeComment(
                success=False, 
                message="Failed to like/unlike comment",
                errors=[str(e)]
            )

class SharePost(graphene.Mutation):
    """Mutation to share a post"""
    class Arguments:
        post_id = graphene.Int(required=True)
        content = graphene.String()  # Optional share message

    success = graphene.Boolean()
    message = graphene.String()
    share = graphene.Field('feed.types.ShareType')
    errors = graphene.List(graphene.String)

    def mutate(self, info, post_id, content=""):
        user = info.context.user
        if not user.is_authenticated:
            return SharePost(
                success=False, 
                message="Authentication required",
                errors=["User must be authenticated to share posts"]
            )

        try:
            post = Post.objects.get(id=post_id, is_deleted=False)
        except Post.DoesNotExist:
            return SharePost(
                success=False, 
                message="Post not found",
                errors=["Post does not exist or has been deleted"]
            )

        # Validate share message length if provided
        if content and len(content) > 500:
            return SharePost(
                success=False, 
                message="Share message too long",
                errors=["Share message cannot exceed 500 characters"]
            )

        try:
            with transaction.atomic():
                share, created = Share.objects.get_or_create(
                    user=user, 
                    post=post,
                    defaults={'content': content.strip() if content else ''}
                )

                if not created:
                    return SharePost(
                        success=False, 
                        message="Post already shared",
                        errors=["You have already shared this post"]
                    )

                return SharePost(
                    success=True, 
                    message="Post shared successfully", 
                    share=share,
                    errors=[]
                )
        except Exception as e:
            return SharePost(
                success=False, 
                message="Failed to share post",
                errors=[str(e)]
            )

class UnsharePost(graphene.Mutation):
    """Mutation to unshare a post"""
    class Arguments:
        post_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    errors = graphene.List(graphene.String)

    def mutate(self, info, post_id):
        user = info.context.user
        if not user.is_authenticated:
            return UnsharePost(
                success=False, 
                message="Authentication required",
                errors=["User must be authenticated to unshare posts"]
            )

        try:
            share = Share.objects.get(user=user, post_id=post_id)
        except Share.DoesNotExist:
            return UnsharePost(
                success=False, 
                message="Share not found",
                errors=["You haven't shared this post"]
            )

        try:
            with transaction.atomic():
                share.delete()
                return UnsharePost(
                    success=True, 
                    message="Post unshared successfully",
                    errors=[]
                )
        except Exception as e:
            return UnsharePost(
                success=False, 
                message="Failed to unshare post",
                errors=[str(e)]
            )

class FollowUser(graphene.Mutation):
    """Mutation to follow/unfollow a user"""
    class Arguments:
        user_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    is_following = graphene.Boolean()
    follower_count = graphene.Int()
    errors = graphene.List(graphene.String)

    def mutate(self, info, user_id):
        user = info.context.user
        if not user.is_authenticated:
            return FollowUser(
                success=False, 
                message="Authentication required",
                errors=["User must be authenticated to follow others"]
            )

        if user.id == user_id:
            return FollowUser(
                success=False, 
                message="Cannot follow yourself",
                errors=["You cannot follow yourself"]
            )

        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return FollowUser(
                success=False, 
                message="User not found",
                errors=["Target user does not exist"]
            )

        try:
            with transaction.atomic():
                follow, created = Follow.objects.get_or_create(
                    follower=user, 
                    following=target_user
                )

                # Get updated follower count
                target_profile = getattr(target_user, 'profile', None)
                follower_count = target_profile.followers_count if target_profile else 0

                if not created:
                    # Unfollow
                    follow.delete()
                    # Refresh follower count after deletion
                    if target_profile:
                        target_profile.refresh_from_db()
                        follower_count = target_profile.followers_count

                    return FollowUser(
                        success=True, 
                        message=f"Unfollowed {target_user.username}", 
                        is_following=False,
                        follower_count=follower_count,
                        errors=[]
                    )

                # Refresh follower count after creation
                if target_profile:
                    target_profile.refresh_from_db()
                    follower_count = target_profile.followers_count

                return FollowUser(
                    success=True, 
                    message=f"Now following {target_user.username}", 
                    is_following=True,
                    follower_count=follower_count,
                    errors=[]
                )
        except Exception as e:
            return FollowUser(
                success=False, 
                message="Failed to follow/unfollow user",
                errors=[str(e)]
            )

class UpdateProfile(graphene.Mutation):
    """Mutation to update user profile"""
    class Arguments:
        bio = graphene.String()
        location = graphene.String()
        birth_date = graphene.Date()
        first_name = graphene.String()
        last_name = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()
    profile = graphene.Field('feed.types.UserProfileType')
    user = graphene.Field('feed.types.UserType')
    errors = graphene.List(graphene.String)

    def mutate(self, info, bio=None, location=None, birth_date=None, first_name=None, last_name=None):
        user = info.context.user
        if not user.is_authenticated:
            return UpdateProfile(
                success=False, 
                message="Authentication required",
                errors=["User must be authenticated to update profile"]
            )

        # Validate inputs
        if bio and len(bio) > 500:
            return UpdateProfile(
                success=False, 
                message="Bio too long",
                errors=["Bio cannot exceed 500 characters"]
            )

        if location and len(location) > 100:
            return UpdateProfile(
                success=False, 
                message="Location too long",
                errors=["Location cannot exceed 100 characters"]
            )

        if first_name and len(first_name) > 30:
            return UpdateProfile(
                success=False, 
                message="First name too long",
                errors=["First name cannot exceed 30 characters"]
            )

        if last_name and len(last_name) > 30:
            return UpdateProfile(
                success=False, 
                message="Last name too long",
                errors=["Last name cannot exceed 30 characters"]
            )

        try:
            with transaction.atomic():
                # Update User model fields
                if first_name is not None:
                    user.first_name = first_name.strip()
                if last_name is not None:
                    user.last_name = last_name.strip()

                if first_name is not None or last_name is not None:
                    user.save()

                # Update or create profile
                profile, created = UserProfile.objects.get_or_create(user=user)

                if bio is not None:
                    profile.bio = bio.strip()
                if location is not None:
                    profile.location = location.strip()
                if birth_date is not None:
                    profile.birth_date = birth_date

                profile.save()

                return UpdateProfile(
                    success=True, 
                    message="Profile updated successfully", 
                    profile=profile,
                    user=user,
                    errors=[]
                )
        except Exception as e:
            return UpdateProfile(
                success=False, 
                message="Failed to update profile",
                errors=[str(e)]
            )

class Mutation(graphene.ObjectType):
    """GraphQL mutations"""

    # Post mutations
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    like_post = LikePost.Field()
    share_post = SharePost.Field()
    unshare_post = UnsharePost.Field()

    # Comment mutations
    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()
    like_comment = LikeComment.Field()

    # User mutations
    follow_user = FollowUser.Field()
    update_profile = UpdateProfile.Field()