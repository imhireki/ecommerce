import json

from model_bakery import baker
import pytest


pytestmark = [pytest.mark.django_db, pytest.mark.integration]


class TestOrderEndpoints:
    endpoint = "/api/v1/orders/"

    def test_order_list(self, api_client, get_order_list_data):
        baker.make("order.Order", 5)
        baker.make("order.OrderItem", 5)

        user = baker.make("User")
        orders = baker.make("order.Order", 2, user=user)
        orders_items = [
            baker.make("order.OrderItem", 2, order=order) for order in orders
        ]

        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(self.endpoint)

        assert response.status_code == 200
        assert json.loads(response.content) == [
            get_order_list_data(orders[1], orders_items[1]),
            get_order_list_data(orders[0], orders_items[0]),
        ]

    def test_checkout(self, api_client, get_checkout_data, patch_image):
        product_variations = baker.make(
            "product.ProductVariation",
            2,
            product=baker.make("product.Product"),
            promotional_price=10,
        )

        user_cart_data = {
            "order_items": [
                {
                    "product": variation.product.id,
                    "product_variation": variation.id,
                    "price": variation.promotional_price,
                    "quantity": variation.id,
                }
                for variation in product_variations
            ]
        }

        client = api_client()
        client.force_authenticate(user=baker.make("User"))
        response = client.post(
            self.endpoint + "checkout/", user_cart_data, format="json"
        )

        assert response.status_code == 201
        assert json.loads(response.content) == get_checkout_data(
            json.loads(response.content)
        )
