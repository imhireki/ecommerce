from model_bakery import baker
import pytest

from apps.notification import tasks


pytestmark = [pytest.mark.unit, pytest.mark.celery]

def test_broadcast_task(celery_session_worker, mocker):
    broadcast = mocker.patch('apps.notification.utils.broadcast')
    b = baker.prepare('notification.Broadcast')
    
    tasks.broadcast_task.delay(b.id, b.message, b.expires_at).get(timeout=5)

    assert broadcast.call_args.args == (b.id, b.message, b.expires_at)

