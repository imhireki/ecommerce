from django_celery_beat.models import PeriodicTask, CrontabSchedule
from model_bakery import baker
import pytest

from apps.notification.models import Broadcast
from apps.notification import utils


pytestmark = [pytest.mark.django_db, pytest.mark.unit]

def test_broadcast(mocker):
    b = baker.make('notification.Broadcast')

    async_to_sync = mocker.patch('apps.notification.utils.async_to_sync')
    broadcast_async = mocker.patch(
        'apps.notification.utils.AsyncBroadcastConsumer.broadcast'
    )

    utils.broadcast(b.id, b.message, b.expires_at)

    assert async_to_sync.call_args.args == (broadcast_async,)
    assert async_to_sync().call_args.args == (b.id, b.message, b.expires_at)

@pytest.mark.parametrize('broadcast', [True, False])
def test_delete_broadcast_object(broadcast):

    if broadcast:
        baker.make('notification.Broadcast')

    utils.delete_broadcast_object(9)

    assert not Broadcast.objects.filter(id=9).exists()

@pytest.mark.parametrize('ptask, same_sched_ptask', [
    (True,True), (True, False), (False, True), (False, False)
])
def test_remove_broadcast_periodic_task(mocker, ptask, same_sched_ptask):
    schedule = None

    if ptask or same_sched_ptask:
        schedule = baker.make('CrontabSchedule')

    if ptask:
        baker.make('PeriodicTask', crontab=schedule, name='b 5')

    if same_sched_ptask:
        baker.make('PeriodicTask', crontab=schedule)

    utils.remove_broadcast_periodic_task(name='b 5')

    if ptask or same_sched_ptask:
        assert (same_sched_ptask == CrontabSchedule.objects
                .filter(id=schedule.id).exists())
    assert not PeriodicTask.objects.filter(name='b 5').exists()

