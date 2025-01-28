import json

from django.urls import reverse
from model_bakery import baker
import pytest

from apps.product import views


pytestmark = [pytest.mark.django_db, pytest.mark.unit]


def test_product_list_view(rf, get_product_list_data, patch_image):
    products = baker.make("product.Product", 2)

    url = reverse("product-list")
    request = rf.get(url)
    product_list_view = views.ProductListView.as_view()

    response = product_list_view(request).render()

    assert response.status_code == 200
    assert len(json.loads(response.content)) == 2
    assert get_product_list_data(products[0]) and get_product_list_data(
        products[1]
    ) in json.loads(response.content)


def test_product_detail_view(rf, get_product_detail_data, patch_image):
    product = baker.make("product.Product")
    images = baker.make("product.ProductImage", 2, product=product)
    variations = baker.make("product.ProductVariation", 2, product=product)

    url = reverse("product-detail", kwargs={"slug": product.slug})
    request = rf.get(url)
    product_detail_view = views.ProductDetailView.as_view()

    response = product_detail_view(request, slug=product.slug).render()

    assert response.status_code == 200
    assert json.loads(response.content) == get_product_detail_data(
        product, images, variations
    )


def test_product_search_view(rf, get_product_list_data, patch_image):
    products = baker.make("product.Product", 3)

    url = reverse("product-search")
    request = rf.post(
        url, content_type="application/json", data={"query": products[0].name}
    )
    product_search_view = views.ProductSearchView.as_view()

    response = product_search_view(request).render()

    assert response.status_code == 200
    assert len(json.loads(response.content)) == 1
    assert get_product_list_data(products[0]) in json.loads(response.content)
