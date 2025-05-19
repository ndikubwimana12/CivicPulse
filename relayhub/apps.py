from django.apps import AppConfig

class RelayhubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relayhub'
    
    def ready(self):
        import relayhub.signals
