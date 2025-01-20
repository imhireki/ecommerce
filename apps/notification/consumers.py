from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import BaseChannelLayer, get_channel_layer


class AsyncBroadcastConsumer(AsyncJsonWebsocketConsumer):
    channel_layer: BaseChannelLayer

    async def connect(self):
        self.group_name = 'broadcast'

        # Add user's channel to group 
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        # Leave group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notification(self, event) -> None:
        """Receive group messages and broadcast it over the WebSocket"""

        await self.send_json({
            'bid': event['bid'],
            'message': event['message'],
            'expires_at': event['expires_at']
        })

    @classmethod
    async def broadcast(cls, bid, message, expires_at) -> None:
        """Send notifications over to the group"""
        channel_layer: BaseChannelLayer = get_channel_layer()  # type: ignore

        await channel_layer.group_send('broadcast', {
            'type': 'notification', 'bid': bid,
            'message': message, 'expires_at': expires_at,
        })

