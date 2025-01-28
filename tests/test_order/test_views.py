import json

from rest_framework.test import force_authenticate
from django.urls import reverse
from model_bakery import baker
import pytest

from apps.order import views


pytestmark = [pytest.mark.django_db, pytest.mark.unit]


def test_order_checkout_view(rf, get_checkout_data, patch_image):
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

    request = rf.post(
        reverse("order-checkout"), content_type="application/json", data=user_cart_data
    )
    force_authenticate(request, user=baker.make("User"))

    order_checkout_view = views.OrderCheckoutView.as_view()
    response = order_checkout_view(request).render()

    assert response.status_code == 201
    assert json.loads(response.content) == get_checkout_data(
        json.loads(response.content)
    )


def test_order_list_view(rf, get_order_list_data):
    baker.make("order.Order", 20)

    user = baker.make("User")
    baker.make("order.Order", 2, user=user)

    url = reverse("order-list")
    request = rf.get(url)
    force_authenticate(request, user=user)
    order_list_view = views.OrderListView.as_view()

    response = order_list_view(request).render()

    assert response.status_code == 200
    assert json.loads(response.content) == [
        get_order_list_data(
            json.loads(response.content)[0],
            json.loads(response.content)[0]["order_items"],
        ),
        get_order_list_data(
            json.loads(response.content)[1],
            json.loads(response.content)[1]["order_items"],
        ),
    ]
