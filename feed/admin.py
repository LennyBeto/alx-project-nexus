from django.contrib import admin
from .models import Post, Comment, Like, Share, Follow

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'content_preview', 'likes_count', 'comments_count', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username']
    readonly_fields = ['likes_count', 'comments_count', 'shares_count', 'created_at', 'updated_at']
    raw_id_fields = ['author']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content Preview"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post', 'content_preview', 'created_at', 'parent']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username', 'post__content']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['author', 'post', 'parent']
    
    def content_preview(self, obj):
        return obj.content[:30] + "..." if len(obj.content) > 30 else obj.content
    content_preview.short_description = "Content Preview"

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'like_type', 'post', 'comment', 'created_at']
    list_filter = ['like_type', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    raw_id_fields = ['user', 'post', 'comment']

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'message_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__content']
    readonly_fields = ['created_at']
    raw_id_fields = ['user', 'post']
    
    def message_preview(self, obj):
        if obj.message:
            return obj.message[:30] + "..." if len(obj.message) > 30 else obj.message
        return "No message"
    message_preview.short_description = "Message Preview"

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']
    readonly_fields = ['created_at']
    raw_id_fields = ['follower', 'following']
