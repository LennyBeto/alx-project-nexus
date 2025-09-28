# feed/signals.py

# Signal handlers are already defined in models.py
# This file imports them to ensure they're registered

from django.apps import apps
from django.db.models.signals import post_save, post_delete

# Import signal handlers from models
if apps.ready:
    from .models import (
        increment_like_count, decrement_like_count,
        increment_comment_count, increment_share_count,
        decrement_share_count, update_follow_counts,
        decrement_follow_counts, update_user_posts_count,
        create_user_profile
    )