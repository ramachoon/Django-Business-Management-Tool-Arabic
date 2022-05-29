from django.apps import AppConfig


class StoreroomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'storeroom'
    verbose_name = 'انبار'

    def ready(self):
        import storeroom.signals
