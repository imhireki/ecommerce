from channels.layers import InMemoryChannelLayer, get_channel_layer
from django.db.models.signals import post_save, pre_delete
from channels.testing import WebsocketCommunicator
import pytest_asyncio
import pytest

from apps.notification import consumers
from apps.notification import signals


@pytest.fixture(autouse=True)
def override_channel_layers(settings):
    settings.CHANNEL_LAYERS = {
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
    }


@pytest_asyncio.fixture
async def bc_communicator():
    c = WebsocketCommunicator(
        consumers.AsyncBroadcastConsumer.as_asgi(), "/ws/notification/broadcast/"
    )
    await c.connect()
    yield c
    await c.disconnect()


@pytest.fixture
def channel_layer() -> InMemoryChannelLayer:
    return get_channel_layer()  # type: ignore


@pytest.fixture(autouse=True)
def disable_broadcast_signals():
    post_save.disconnect(signals.post_save_broadcast, sender="notification.Broadcast")
    pre_delete.disconnect(signals.pre_delete_broadcast, sender="notification.Broadcast")

    yield

    post_save.connect(signals.post_save_broadcast, sender="notification.Broadcast")
    pre_delete.connect(signals.pre_delete_broadcast, sender="notification.Broadcast")


@pytest.fixture
def enable_post_save_broadcast():
    post_save.connect(signals.post_save_broadcast, sender="notification.Broadcast")


@pytest.fixture
def enable_pre_delete_broadcast():
    pre_delete.connect(signals.pre_delete_broadcast, sender="notification.Broadcast")
