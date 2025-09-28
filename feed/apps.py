from django.apps import AppConfig


class FeedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feed'
    verbose_name = 'Social Media Feed'

    def ready(self):
        try:
            import feed.signals  # Import signal handlers
        except ImportError:
            pass  