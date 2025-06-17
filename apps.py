from django.apps import AppConfig

class AiToolsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_tools'
    verbose_name = 'AI Tools'
    
    def ready(self):
        # Import and connect signals
        try:
            from . import signals
        except ImportError:
            pass