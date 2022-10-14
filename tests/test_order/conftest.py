import pytest


@pytest.fixture
def get_order_list_data():
    return lambda order, order_items: {
        "id": order.id,
        "paid_amount": order.paid_amount,
        "status": order.status,
        "items": [{
            "id": order_item.id,
            "product": {
                "name": order_item.product.name,
                "thumbnail_url": "",
            },
            "product_variation": {
                "name": order_item.product_variation.name,
                "price": order_item.product_variation.price,
                "promotional_price": order_item.product_variation.\
                                     promotional_price
            },
        } for order_item in order_items]
    }

@pytest.fixture
def get_checkout_data():
    return lambda product_variations: {
        "id": "AbhDs-KLLzo-OZDh",
        "price": sum([
            variation.promotional_price
            for variation in product_variations
        ]),
        "status": "Created",
    }

