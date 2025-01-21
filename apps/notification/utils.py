from django_celery_beat.models import PeriodicTask
from django.db.models import ObjectDoesNotExist
from asgiref.sync import async_to_sync 

from .consumers import AsyncBroadcastConsumer
from .models import Broadcast


def broadcast(bid, message, expires_at) -> None:
    async_to_sync(AsyncBroadcastConsumer.broadcast)(bid, message, expires_at)

def delete_broadcast_object(bid):
    try:
        broadcast = Broadcast.objects.get(id=bid)
    except ObjectDoesNotExist:
        return
    broadcast.delete()

def remove_broadcast_periodic_task(name: str) -> None:
    try:
        periodic_task = PeriodicTask.objects.get(name=name)
    except ObjectDoesNotExist:
        return

    schedule = periodic_task.crontab

    periodic_task.delete()

    # Schedule being reused
    if PeriodicTask.objects.filter(crontab=schedule).exists():
        return

    schedule.delete()

