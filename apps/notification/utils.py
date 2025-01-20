from asgiref.sync import async_to_sync 

from .consumers import AsyncBroadcastConsumer


def broadcast(bid, message, expires_at) -> None:
    async_to_sync(AsyncBroadcastConsumer.broadcast)(bid, message, expires_at)

