from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

from django.apps import AppConfig

class CoreConfig(AppConfig):  # Make sure this class name matches your app config
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'  # Ensure this is your app name

    def ready(self):
        import core.signals  #  Import signals when the app starts
