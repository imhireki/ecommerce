import os

from celery import Celery


# set DJANGO_SETTINGS_MODULE=core.settings for celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("ecommerce")

# Source CELERY_* configs from django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Modules to search for tasks.py
app.autodiscover_tasks(["apps.order", "apps.product", "apps.notification"])


@app.task(bind=True, ignore_results=True)
def debug_task(self):
    print(f"request {self.request!r}")
