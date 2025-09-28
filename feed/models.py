# feed/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
 

class UserProfile(models.Model):
    """Extended user profile with additional fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    followers_count = models.PositiveIntegerField(default=0, db_index=True)
    following_count = models.PositiveIntegerField(default=0, db_index=True)
    posts_count = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        indexes = [
            models.Index(fields=['-followers_count']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username}'s profile"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username


class Post(models.Model):
    """Post model with content and interaction tracking"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=2000)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    
    # Denormalized counters for performance
    likes_count = models.PositiveIntegerField(default=0, db_index=True)
    comments_count = models.PositiveIntegerField(default=0, db_index=True)
    shares_count = models.PositiveIntegerField(default=0, db_index=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Soft delete
    is_deleted = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = 'posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'is_deleted']),
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['-likes_count']),
        ]

    def __str__(self):
        return f"Post by {self.author.username}: {self.content[:50]}..."

    def delete(self, using=None, keep_parents=False):
        """Soft delete implementation"""
        self.is_deleted = True
        self.save(using=using)


class Comment(models.Model):
    """Comment model with nested replies support"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField(max_length=1000)
    
    # Interaction counters
    likes_count = models.PositiveIntegerField(default=0, db_index=True)
    replies_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Soft delete
    is_deleted = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', '-created_at']),
            models.Index(fields=['parent', '-created_at']),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.id}: {self.content[:30]}..."

    def delete(self, using=None, keep_parents=False):
        """Soft delete implementation"""
        self.is_deleted = True
        self.save(using=using)


class Like(models.Model):
    """Like model for posts and comments"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'likes'
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_post_like'),
            models.UniqueConstraint(fields=['user', 'comment'], name='unique_comment_like'),
            models.CheckConstraint(
                check=models.Q(post__isnull=False) | models.Q(comment__isnull=False),
                name='like_either_post_or_comment'
            )
        ]
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['comment', 'created_at']),
        ]

    def __str__(self):
        target = self.post or self.comment
        return f"Like by {self.user.username} on {target}"


class Share(models.Model):
    """Share model for post sharing"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    content = models.TextField(max_length=500, blank=True)  # Optional share message
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shares'
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_post_share')
        ]
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"Share by {self.user.username} of post {self.post.id}"


class Follow(models.Model):
    """Follow relationship model"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'follows'
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_follow'),
            models.CheckConstraint(
                check=~models.Q(follower=models.F('following')),
                name='no_self_follow'
            )
        ]
        indexes = [
            models.Index(fields=['follower', 'created_at']),
            models.Index(fields=['following', 'created_at']),
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


# Signal handlers for maintaining denormalized counters
@receiver(post_save, sender=Like)
def increment_like_count(sender, instance, created, **kwargs):
    """Increment like count when a like is created"""
    if created:
        if instance.post:
            Post.objects.filter(id=instance.post.id).update(likes_count=models.F('likes_count') + 1)
        elif instance.comment:
            Comment.objects.filter(id=instance.comment.id).update(likes_count=models.F('likes_count') + 1)


@receiver(post_delete, sender=Like)
def decrement_like_count(sender, instance, **kwargs):
    """Decrement like count when a like is deleted"""
    if instance.post:
        Post.objects.filter(id=instance.post.id).update(likes_count=models.F('likes_count') - 1)
    elif instance.comment:
        Comment.objects.filter(id=instance.comment.id).update(likes_count=models.F('likes_count') - 1)


@receiver(post_save, sender=Comment)
def increment_comment_count(sender, instance, created, **kwargs):
    """Increment comment count when a comment is created"""
    if created and not instance.is_deleted:
        Post.objects.filter(id=instance.post.id).update(comments_count=models.F('comments_count') + 1)
        if instance.parent:
            Comment.objects.filter(id=instance.parent.id).update(replies_count=models.F('replies_count') + 1)


@receiver(post_save, sender=Share)
def increment_share_count(sender, instance, created, **kwargs):
    """Increment share count when a share is created"""
    if created:
        Post.objects.filter(id=instance.post.id).update(shares_count=models.F('shares_count') + 1)


@receiver(post_delete, sender=Share)
def decrement_share_count(sender, instance, **kwargs):
    """Decrement share count when a share is deleted"""
    Post.objects.filter(id=instance.post.id).update(shares_count=models.F('shares_count') - 1)


@receiver(post_save, sender=Follow)
def update_follow_counts(sender, instance, created, **kwargs):
    """Update follower/following counts"""
    if created:
        UserProfile.objects.filter(user=instance.following).update(followers_count=models.F('followers_count') + 1)
        UserProfile.objects.filter(user=instance.follower).update(following_count=models.F('following_count') + 1)


@receiver(post_delete, sender=Follow)
def decrement_follow_counts(sender, instance, **kwargs):
    """Decrement follower/following counts"""
    UserProfile.objects.filter(user=instance.following).update(followers_count=models.F('followers_count') - 1)
    UserProfile.objects.filter(user=instance.follower).update(following_count=models.F('following_count') - 1)


@receiver(post_save, sender=Post)
def update_user_posts_count(sender, instance, created, **kwargs):
    """Update user's posts count"""
    if created and not instance.is_deleted:
        UserProfile.objects.filter(user=instance.author).update(posts_count=models.F('posts_count') + 1)


# Create user profile automatically
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile when user is created"""
    if created:
        UserProfile.objects.create(user=instance)
