from django.apps import AppConfig

class AiToolsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_tools'
    
    def ready(self):
        # Import and connect signals
        from . import signals