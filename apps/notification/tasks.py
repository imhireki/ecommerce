from celery import shared_task

from . import utils


@shared_task
def broadcast_task(bid, message, expires_at) -> None:
    """Triggered at scheduled_to"""
    utils.broadcast(bid, message, expires_at)


@shared_task
def broadcast_cleanup_task(bid) -> None:
    """Triggered at expires_at"""

    # Remove periodic tasks
    utils.remove_broadcast_periodic_task(f"broadcast {bid}")
    utils.remove_broadcast_periodic_task(f"broadcast_cleanup {bid}")

    # Delete my Broadcast object
    utils.delete_broadcast_object(bid)
