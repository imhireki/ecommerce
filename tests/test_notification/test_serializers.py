from model_bakery import baker
import pytest

from apps.notification import serializers


pytestmark = [pytest.mark.django_db, pytest.mark.unit]

class TestBroadcastSerializer:
    def test_serialize(self):
        broadcast = baker.make('notification.Broadcast')

        serializer = serializers.BroadcastSerializer(broadcast)

        expires_at = broadcast.expires_at.isoformat().replace('+00:00', 'Z')
        expected_data = {
            'id': broadcast.id,
            'message': broadcast.message,
            'expires_at': expires_at
        }

        assert serializer.data == expected_data

