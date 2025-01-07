from rest_framework.serializers import DateTimeField
from django.db.models.signals import post_save
from apps.order.signals import post_save_order
import pytest


@pytest.fixture
def get_order_list_data():
    def _(order, order_items):
        if not isinstance(order, dict):
            order = order.__dict__
            order_items = [
                order_item.__dict__
                for order_item in order_items
            ]
        return {
            "id": str(order['id']),
            "paid_amount": str(order['paid_amount']),
            "status": "Pending",
            "created_at": DateTimeField().\
                          to_representation(order['created_at']),
            "order_items": [{
                "id": order_item['id'],
                "product": order_item['product'],
                "product_variation": order_item['product_variation'],
                "price": str(order_item['price']),
                "quantity": order_item['quantity'],
            } for order_item in order_items],
        }
    return _

@pytest.fixture
def get_checkout_data():
    def _(order):
        if not isinstance(order, dict):
            order = order.__dict__
        return {
            "id": str(order['id']),
            "paid_amount": str(order['paid_amount']),
            "status": "Pending",
        }
    return _

@pytest.fixture(autouse=True)
def disable_post_save_signal():
    # Disconnect the signal temporarily for the test
    post_save.disconnect(post_save_order, sender='order.Order')
    yield
    # Reconnect the signal after the test
    post_save.connect(post_save_order, sender='order.Order')

@pytest.fixture
def enable_post_save_signal():
    post_save.connect(post_save_order, sender='order.Order')
    yield
    post_save.disconnect(post_save_order, sender='order.Order')

