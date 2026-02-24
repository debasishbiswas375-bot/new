import sys
from django.apps import AppConfig

class ConverterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'converter'

    def ready(self):
        # Import signals so new users get profiles automatically
        import converter.signals
        
        # Self-Healing logic for existing users (admin, deba, etc.)
        # We only run this if we are starting the actual web server
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv or 'mysite.wsgi' in sys.argv:
            from django.contrib.auth.models import User
            try:
                from .models import UserProfile
                for user in User.objects.all():
                    # Check if profile exists; if not, create it
                    if not hasattr(user, 'profile'):
                        UserProfile.objects.get_or_create(user=user)
            except Exception:
                pass
