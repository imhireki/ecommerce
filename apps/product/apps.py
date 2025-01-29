from django.apps import AppConfig


class ProductConfig(AppConfig):
    name = "apps.product"

    def ready(self):
        """Ensure signals aren't prematurely loaded."""
        import apps.product.signals
