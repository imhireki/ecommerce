from celery import shared_task

from . import utils


@shared_task
def broadcast_task(bid, message, expires_at) -> None:
    """Triggered at scheduled_to"""
    utils.broadcast(bid, message, expires_at)

