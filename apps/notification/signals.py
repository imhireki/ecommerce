from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

from . import tasks
from . import utils


@receiver(post_save, sender='notification.Broadcast')
def post_save_broadcast(instance, **kwargs):
    """Schedule the broadcasting and cleanup of the schedled tasks"""
    current_time = timezone.now()
    margin_of_error = timedelta(minutes=1)

    # There's not enough time to schedule the broadcasting
    if instance.scheduled_to <= current_time + margin_of_error:
        # Execute in the present
        tasks.broadcast_task.delay(
            instance.id,
            instance.message,
            instance.expires_at.isoformat()
        )
    else:
        # Schedule for the future
        utils.schedule_broadcast(
            instance.id,
            instance.message,
            instance.scheduled_to,
            instance.expires_at
        )

    # There's not enough time to schedule the cleanup
    if instance.expires_at <= current_time + margin_of_error:
        tasks.broadcast_cleanup_task.delay(instance.id)
    else:
        utils.schedule_broadcast_cleanup(
            instance.id, instance.expires_at
        )

