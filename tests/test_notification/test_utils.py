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

