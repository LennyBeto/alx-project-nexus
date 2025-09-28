from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Post, Comment, Like, Share, Follow, UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline for UserProfile in User admin"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    extra = 0
    fields = ('bio', 'location', 'birth_date', 'avatar', 'followers_count', 'following_count', 'posts_count')
    readonly_fields = ('followers_count', 'following_count', 'posts_count')


class CustomUserAdmin(UserAdmin):
    """Extended User admin with profile inline"""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model"""
    list_display = ('user', 'followers_count', 'following_count', 'posts_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'bio', 'location')
    readonly_fields = ('followers_count', 'following_count', 'posts_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Information', {
            'fields': ('bio', 'location', 'birth_date', 'avatar')
        }),
        ('Statistics', {
            'fields': ('followers_count', 'following_count', 'posts_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin for Post model"""
    list_display = ('id', 'author', 'content_preview', 'likes_count', 'comments_count', 'shares_count', 'created_at', 'is_deleted')
    list_filter = ('created_at', 'is_deleted')
    search_fields = ('content', 'author__username')
    readonly_fields = ('likes_count', 'comments_count', 'shares_count', 'created_at', 'updated_at')
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Post Information', {
            'fields': ('author', 'content', 'image')
        }),
        ('Statistics', {
            'fields': ('likes_count', 'comments_count', 'shares_count'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_deleted',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    actions = ['soft_delete_posts', 'restore_posts']
    
    def soft_delete_posts(self, request, queryset):
        updated = queryset.update(is_deleted=True)
        self.message_user(request, f'{updated} posts were soft deleted.')
    soft_delete_posts.short_description = 'Soft delete selected posts'
    
    def restore_posts(self, request, queryset):
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f'{updated} posts were restored.')
    restore_posts.short_description = 'Restore selected posts'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin for Comment model"""
    list_display = ('id', 'author', 'post', 'parent', 'content_preview', 'likes_count', 'created_at', 'is_deleted')
    list_filter = ('created_at', 'is_deleted')
    search_fields = ('content', 'author__username', 'post__content')
    readonly_fields = ('likes_count', 'replies_count', 'created_at', 'updated_at')
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'author', 'parent', 'content')
        }),
        ('Statistics', {
            'fields': ('likes_count', 'replies_count'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_deleted',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Admin for Like model"""
    list_display = ('id', 'user', 'get_target', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    def get_target(self, obj):
        if obj.post:
            return format_html('<a href="/admin/feed/post/{}/change/">Post: {}</a>', 
                             obj.post.id, obj.post.content[:30])
        elif obj.comment:
            return format_html('<a href="/admin/feed/comment/{}/change/">Comment: {}</a>', 
                             obj.comment.id, obj.comment.content[:30])
        return 'Unknown'
    get_target.short_description = 'Target'
    get_target.allow_tags = True


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    """Admin for Share model"""
    list_display = ('id', 'user', 'post', 'content_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__content', 'content')
    readonly_fields = ('created_at',)
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        if obj.content:
            return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content
        return '(No message)'
    content_preview.short_description = 'Share Message'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Admin for Follow model"""
    list_display = ('id', 'follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'following__username')
    readonly_fields = ('created_at',)
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('follower', 'following')


# Customize admin site
admin.site.site_header = 'Social Media Feed Administration'
admin.site.site_title = 'Social Media Admin'
admin.site.index_title = 'Welcome to Social Media Feed Administration'