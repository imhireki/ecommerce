from rest_framework.serializers import DateTimeField
import pytest


@pytest.fixture
def get_order_list_data():
    return lambda order, order_items: {
        "id": str(order.id),
        "paid_amount": str(order.paid_amount),
        "status": order.get_status_display(),
        "created_at": DateTimeField().to_representation(order.created_at),
        "order_items": [{
            "id": order_item.id,
            "product": order_item.product,
            "product_variation": order_item.product_variation,
            "price": str(order_item.price),
            "quantity": order_item.quantity,
        } for order_item in order_items],
    }

@pytest.fixture
def get_checkout_data():
    return lambda order: {
        "id": str(order.id),
        "paid_amount": str(order.paid_amount),
        "status": order.get_status_display(),
    }

