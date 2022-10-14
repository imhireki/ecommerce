import json

from django_mock_queries.mocks import MockSet
from model_bakery import baker
import pytest


pytestmark = [pytest.mark.django_db, pytest.mark.e2e]


class TestOrderEndpoints:  
    endpoint = '/api/v1/orders/'

    def test_order_list(self, api_client, get_order_list_data):
        baker.make('orders.Order', 10)
        baker.make('orders.OrderItem', 10)

        user = baker.make('django.contrib.auth.models.User')
        order = baker.make('orders.Order', user=user)
        order_items = baker.make('orders.OrderItem', 5, order=order)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2
        assert get_order_list_data(order, order_items) \
               == json.loads(response.content)


