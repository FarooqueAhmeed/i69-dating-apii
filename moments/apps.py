from django.apps import AppConfig


class MomentsConfig(AppConfig):
    name = "moments"

    def ready(self):
        import moments.signals
