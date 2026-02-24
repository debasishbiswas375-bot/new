from django.apps import AppConfig

class ConverterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'converter'

    def ready(self):
        # This imports the signals when the app starts
        import converter.signals
