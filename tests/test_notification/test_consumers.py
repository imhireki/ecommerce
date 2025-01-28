from channels.testing import WebsocketCommunicator
import pytest

from apps.notification import consumers


pytestmark = [pytest.mark.asyncio, pytest.mark.django_db, pytest.mark.integration]


class TestAsyncBroadcastConsumer:
    async def test_connect(self, channel_layer):
        communicator = WebsocketCommunicator(
            consumers.AsyncBroadcastConsumer.as_asgi(),
            "/ws/notification/broadcast/",
        )
        connected, _ = await communicator.connect()

        assert connected
        assert "broadcast" in channel_layer.groups

    async def test_disconnect(self, bc_communicator, channel_layer):
        await bc_communicator.disconnect()

        assert "broadcast" not in channel_layer.groups

    async def test_notification(self, bc_communicator, channel_layer):
        notification = {"bid": 1, "message": "message", "expires_at": 1}

        await channel_layer.group_send(
            "broadcast", {"type": "notification", **notification}
        )
        ws_message = await bc_communicator.receive_json_from()

        assert ws_message == notification

    async def test_broadcast(self, bc_communicator):
        notification = {"bid": 1, "message": "message", "expires_at": 1}

        await consumers.AsyncBroadcastConsumer.broadcast(**notification)
        ws_message = await bc_communicator.receive_json_from()

        assert ws_message == notification
