import json

from django_mock_queries.mocks import MockSet
from model_bakery import baker
import pytest


pytestmark = [pytest.mark.django_db, pytest.mark.e2e]


class TestOrderEndpoints:  
    endpoint = '/api/v1/orders/'

    def test_order_list(self, api_client, get_order_list_data):
        baker.make('order.Order', 10)
        baker.make('order.OrderItem', 10)

        orders = baker.make('order.Order', 2, user=baker.make('User'))
        orders_items = [
            baker.make('order.OrderItem', 2, order=order)
            for order in orders
        ]

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2
        assert get_order_list_data(orders[0], orders_items[0]) \
            and get_order_list_data(orders[1], orders_items[1]) \
            == json.loads(response.content)

    def test_checkout(self, mocker, api_client,
                      patch_image, get_checkout_data):
        product_variations = baker.make(
            'product.ProductVariation', 2,
            product=baker.make('product.Product'),
            promotional_price=10)

        mocker.patch('apps.product.views.CheckoutView.get_queryset',
                     return_value=MockSet(*product_variations))

        user_cart_data = [{
            "product": variation.product.id,
            "product_variation": variation.id,
            "price": variation.promotional_price,
            "quantity": variation.id
        } for variation in product_variations]

        response = api_client().post(
            self.endpoint,
            json.dumps(user_cart_data),
            format='json')

        assert response.status_code == 201
        assert json.loads(response.content) \
               == get_checkout_data(product_variations)

