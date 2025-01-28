from model_bakery import baker
import pytest

from apps.order import serializers


pytestmark = [pytest.mark.django_db, pytest.mark.unit]


class TestOrderCheckoutSerializer:
    def test_deserialize(self, get_checkout_data, patch_image):
        product_variations = baker.make(
            "product.ProductVariation",
            2,
            product=baker.make("product.Product"),
            promotional_price=10,
        )

        order_items_data = [
            {
                "product": variation.product.id,
                "product_variation": variation.id,
                "price": variation.promotional_price,
                "quantity": variation.id,
            }
            for variation in product_variations
        ]

        valid_data = {
            "user": baker.make("User").id,
            "order_items": order_items_data,
            "paid_amount": sum(
                [product_variation["price"] for product_variation in order_items_data]
            ),
        }

        serializer = serializers.OrderCheckoutSerializer(data=valid_data)
        serializer.is_valid()
        order = serializer.save()

        assert order
        assert serializer.errors == {}
        assert serializer.data == get_checkout_data(order)


class TestOrderListSerializer:
    def test_serialize(self, get_order_list_data):
        order = baker.make("order.Order")
        order_items = baker.make("order.OrderItem", 2, order=order)

        serializer = serializers.OrderListSerializer(order)

        assert serializer.data == get_order_list_data(order, order_items)
