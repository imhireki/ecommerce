import json

from django.utils import timezone
from django.urls import reverse
from datetime import timedelta
from model_bakery import baker
import pytest

from apps.notification.views import BroadcastListView


pytestmark = [pytest.mark.django_db, pytest.mark.unit]


def test_broadcast_list_view(rf):
    # Broadcasted
    broadcasts = baker.make(
        "notification.Broadcast", 3, scheduled_to=timezone.now() - timedelta(days=1)
    )

    # Noise (to be broadcasted)
    baker.make(
        "notification.Broadcast", 2, scheduled_to=timezone.now() + timedelta(days=1)
    )

    url = reverse("broadcast-notification-list")
    request = rf.get(url)
    view = BroadcastListView.as_view()
    response = view(request).render()

    expected_response = [
        {
            "id": n.id,
            "message": n.message,
            "expires_at": n.expires_at.isoformat().replace("+00:00", "Z"),
        }
        for n in broadcasts
    ]

    assert response.status_code == 200
    assert json.loads(response.content) == expected_response
