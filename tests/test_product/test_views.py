from django.urls import reverse
from model_bakery import baker
import pytest
import json

from apps.product import views


pytestmark = [pytest.mark.django_db, pytest.mark.unit]

@pytest.fixture(autouse=True)
def patch_resize_image(mocker):
    mocker.patch('apps.product.utils.resize_image', lambda image, size: image)
    

def test_product_list_view(mocker, rf):
    mocker.patch('apps.product.models.Product.get_thumbnail_absolute_url')
    baker.make('product.Product', 3)

    url = reverse('product-list')
    request = rf.get(url)
    product_list_view = views.ProductListView.as_view()

    response = product_list_view(request).render()

    assert response.status_code == 200
    assert len(json.loads(response.content)) == 3

def test_product_detail_view(mocker, rf):
    product = baker.make('product.Product')

    url = reverse('product-detail', kwargs={"slug": product.slug})
    request = rf.get(url)
    product_detail_view = views.ProductDetailView.as_view()

    response = product_detail_view(request, slug=product.slug).render()

    assert response.status_code == 200
    assert json.loads(response.content)

def test_product_search_view(mocker, rf):
    mocker.patch('apps.product.models.Product.get_thumbnail_absolute_url')
    product = baker.make('product.Product', 3)
    
    url = reverse('product-search')
    request = rf.post(url, content_type='application/json',
                      data={"query": product[0].name})
    product_search_view = views.ProductSearchView.as_view()

    response = product_search_view(request).render()

    assert response.status_code == 200
    assert json.loads(response.content)

