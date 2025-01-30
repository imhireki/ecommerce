import json

from django_celery_beat.models import PeriodicTask, CrontabSchedule
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


def schedule_broadcast(bid, message, scheduled_to, expires_at) -> None:
    schedule, _ = CrontabSchedule.objects.get_or_create(  # type: ignore
        minute=scheduled_to.minute,
        hour=scheduled_to.hour,
        day_of_month=scheduled_to.day,
        month_of_year=scheduled_to.month,
    )

    periodic_task = PeriodicTask.objects.create(
        name=f"broadcast {bid}",
        task="apps.notification.tasks.broadcast_task",
        one_off=True,  # Runs only once at the scheduled date
        crontab=schedule,
        args=json.dumps([bid, message, expires_at.isoformat()]),
    )
    periodic_task.save()


def schedule_broadcast_cleanup(bid, expires_at) -> None:
    schedule, _ = CrontabSchedule.objects.get_or_create(  # type: ignore
        minute=expires_at.minute,
        hour=expires_at.hour,
        day_of_month=expires_at.day,
        month_of_year=expires_at.month,
    )

    periodic_task = PeriodicTask.objects.create(
        name=f"broadcast_cleanup {bid}",
        task="apps.notification.tasks.broadcast_cleanup_task",
        one_off=True,
        crontab=schedule,
        args=json.dumps([bid]),
    )
    periodic_task.save()
