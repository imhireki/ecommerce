import json

from model_bakery import baker

import pytest


pytestmark = [pytest.mark.django_db, pytest.mark.integration]


class TestNotificationEndpoints:
    endpoint = "/api/v1/notifications/"

    def test_broadcasted(self, api_client):
        broadcasts = baker.make("notification.Broadcast", 3)

        client = api_client()
        response = client.get(self.endpoint + "broadcasted/")

        expected_response = [
            {
                "id": b.id,
                "message": b.message,
                "expires_at": b.expires_at.isoformat().replace("+00:00", "Z"),
            }
            for b in broadcasts[::-1]
        ]

        assert response.status_code == 200
        assert json.loads(response.content) == expected_response
