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

    def test_checkout(self, mocker, api_client,
                      patch_image, get_checkout_data):
        product_variations = baker.prepare(
            'product.ProductVariation', 2,
            product=baker.make('product.Product'))

        mocker.patch('apps.product.views.CheckoutView.get_queryset',
                     return_value=MockSet(*product_variations))

        user_cart_data = [
            {"variation": product_variations[0].id, "quantity": 1},
            {"variation": product_variations[1].id, "quantity": 2}
        ]

        response = api_client().post(
            self.endpoint,
            json.dumps(user_cart_data),
            format='json')

        assert response.status_code == 201
        assert json.loads(response.content) == get_checkout_data(product_variations)

