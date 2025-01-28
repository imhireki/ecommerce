from model_bakery import baker
import pytest

from apps.notification import tasks


pytestmark = [pytest.mark.unit, pytest.mark.celery]


def test_broadcast_task(celery_session_worker, mocker):
    broadcast = mocker.patch("apps.notification.utils.broadcast")
    b = baker.prepare("notification.Broadcast")

    tasks.broadcast_task.delay(b.id, b.message, b.expires_at).get(timeout=5)

    broadcast.assert_called_with(b.id, b.message, b.expires_at)


def test_broadcast_cleanup_task(celery_session_worker, mocker):
    b = baker.prepare("notification.Broadcast", id=10)

    remove_ptask = mocker.patch(
        "apps.notification.utils.remove_broadcast_periodic_task"
    )
    delete_broadcast = mocker.patch("apps.notification.utils.delete_broadcast_object")

    tasks.broadcast_cleanup_task.delay(b.id).get(timeout=5)

    remove_ptask.assert_any_call("broadcast 10")
    remove_ptask.assert_any_call("broadcast_cleanup 10")
    delete_broadcast.assert_called_with(b.id)
