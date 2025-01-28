from django.db.models.signals import post_save, pre_delete
from django.utils.timezone import now
from datetime import timedelta
from model_bakery import baker
import pytest

from apps.notification.models import Broadcast


pytestmark = [pytest.mark.django_db, pytest.mark.unit]


@pytest.mark.parametrize(
    "time, b",
    [
        ("past", baker.prepare(Broadcast, scheduled_to=now() - timedelta(minutes=1))),
        ("present", baker.prepare(Broadcast, scheduled_to=now())),
        ("future", baker.prepare(Broadcast, scheduled_to=now() + timedelta(minutes=3))),
    ],
)
def test_post_save_broadcast_notification(enable_post_save_broadcast, mocker, time, b):
    broadcast_task = mocker.patch("apps.notification.tasks.broadcast_task.delay")

    schedule_broadcast = mocker.patch("apps.notification.utils.schedule_broadcast")

    # Cleanup will also be called, but not tested
    mocker.patch("apps.notification.tasks.broadcast_cleanup_task.delay")
    mocker.patch("apps.notification.utils.schedule_broadcast_cleanup")

    post_save.send(Broadcast, instance=b)

    if time in ["past", "present"]:
        broadcast_task.assert_called_with(b.id, b.message, b.expires_at.isoformat())
    else:
        schedule_broadcast.assert_called_with(
            b.id, b.message, b.scheduled_to, b.expires_at
        )


@pytest.mark.parametrize(
    "time, b",
    [
        ("past", baker.prepare(Broadcast, expires_at=now() - timedelta(minutes=1))),
        ("present", baker.prepare(Broadcast, expires_at=now())),
        ("future", baker.prepare(Broadcast, expires_at=now() + timedelta(minutes=3))),
    ],
)
def test_post_save_broadcast_notification_cleanup(
    enable_post_save_broadcast, mocker, time, b
):
    cleanup_task = mocker.patch("apps.notification.tasks.broadcast_cleanup_task.delay")
    schedule_cleanup = mocker.patch(
        "apps.notification.utils.schedule_broadcast_cleanup"
    )

    # Broadcasting will be called but not tested
    mocker.patch("apps.notification.tasks.broadcast_task.delay")
    mocker.patch("apps.notification.utils.schedule_broadcast")

    post_save.send(Broadcast, instance=b)

    if time in ["past", "present"]:
        cleanup_task.assert_called_with(b.id)
    else:
        schedule_cleanup.assert_called_with(b.id, b.expires_at)


def test_pre_delete_broadcast_notification(enable_pre_delete_broadcast, mocker):
    cleanup = mocker.patch("apps.notification.tasks.broadcast_cleanup_task.delay")

    b = baker.make("notification.Broadcast")

    pre_delete.send(Broadcast, instance=b)

    cleanup.assert_called_with(b.id)
