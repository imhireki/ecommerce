from channels.layers import InMemoryChannelLayer, get_channel_layer
from channels.testing import WebsocketCommunicator
import pytest_asyncio
import pytest

from apps.notification import consumers


@pytest.fixture(autouse=True)
def override_channel_layers(settings):
    # TODO: move to conftest
    settings.CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }

@pytest_asyncio.fixture
async def bc_communicator():
    c = WebsocketCommunicator(
        consumers.AsyncBroadcastConsumer.as_asgi(),
        '/ws/notification/broadcast/', 
    )
    await c.connect()
    yield c
    await c.disconnect()


@pytest.fixture
def channel_layer() -> InMemoryChannelLayer:
    return get_channel_layer()  # type: ignore

