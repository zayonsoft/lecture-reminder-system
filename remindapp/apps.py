from django.apps import AppConfig


class RemindappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'remindapp'
    
    def ready(self):
        import remindapp.signals
