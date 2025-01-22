from django.apps import AppConfig


class NotificationConfig(AppConfig):
    name = 'apps.notification'

    def ready(self):
        """Ensure signals aren't prematurely loaded."""
        import apps.notification.signals

