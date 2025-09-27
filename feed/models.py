# feed/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Denormalized fields for performance
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}..."

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Support for nested comments (replies)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return f"{self.author.username} on {self.post.id}: {self.content[:30]}..."

class Like(models.Model):
    LIKE_TYPES = [
        ('POST', 'Post'),
        ('COMMENT', 'Comment'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')
    like_type = models.CharField(max_length=10, choices=LIKE_TYPES)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        # Ensure a user can only like a post/comment once
        unique_together = [
            ['user', 'post'],
            ['user', 'comment'],
        ]
        indexes = [
            models.Index(fields=['user', 'post']),
            models.Index(fields=['user', 'comment']),
        ]
    
    def save(self, *args, **kwargs):
        # Set like_type based on what's being liked
        if self.post:
            self.like_type = 'POST'
        elif self.comment:
            self.like_type = 'COMMENT'
        super().save(*args, **kwargs)
        
        # Update counters
        if self.like_type == 'POST' and self.post:
            self.post.likes_count = self.post.likes.count()
            self.post.save(update_fields=['likes_count'])
    
    def delete(self, *args, **kwargs):
        post = self.post
        super().delete(*args, **kwargs)
        
        # Update counters after deletion
        if post:
            post.likes_count = post.likes.count()
            post.save(update_fields=['likes_count'])
    
    def __str__(self):
        if self.post:
            return f"{self.user.username} likes post {self.post.id}"
        return f"{self.user.username} likes comment {self.comment.id}"

class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    created_at = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=True, null=True)  # Optional message when sharing
    
    class Meta:
        unique_together = ['user', 'post']  # Prevent duplicate shares
        indexes = [
            models.Index(fields=['user', 'post']),
            models.Index(fields=['post', '-created_at']),
        ]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update share count
        self.post.shares_count = self.post.shares.count()
        self.post.save(update_fields=['shares_count'])
    
    def delete(self, *args, **kwargs):
        post = self.post
        super().delete(*args, **kwargs)
        # Update share count after deletion
        post.shares_count = post.shares.count()
        post.save(update_fields=['shares_count'])
    
    def __str__(self):
        return f"{self.user.username} shared post {self.post.id}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['follower', 'following']
        indexes = [
            models.Index(fields=['follower']),
            models.Index(fields=['following']),
        ]
    
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
