from django.apps import AppConfig

class ConverterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'converter'

    def ready(self):
        # 1. Import signals
        import converter.signals
        
        # 2. Self-Healing: Create missing profiles for existing users
        from django.contrib.auth.models import User
        try:
            from .models import UserProfile
            # This logic runs once every time the server starts
            for user in User.objects.all():
                if not hasattr(user, 'profile'):
                    UserProfile.objects.get_or_create(user=user)
        except Exception:
            # This prevents build errors during the first-time migration
            pass
