# Make sure the celery app is always imported when Django starts
# Making it ready for @shared_tasks
from .celery import app as celery_app


__ALL__ = ('celery_app',)

