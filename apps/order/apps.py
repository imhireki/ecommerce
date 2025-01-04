from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = 'apps.order'

    def ready(self):
        """Ensure signals aren't prematurely loaded."""
        import apps.order.signals

