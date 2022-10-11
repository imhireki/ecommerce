from rest_framework.test import APIClient
from django.conf import settings
import pytest


@pytest.fixture
def api_client():
    return APIClient

@pytest.fixture
def patch_image(mocker):
    mocker.patch('apps.product.utils.resize_image',
                 lambda image, size: image)
    mocker.patch('apps.product.models.Product.get_thumbnail_absolute_url',
                 settings.ABSOLUTE_URL + '/media/thumbnail')
    mocker.patch('apps.product.models.ProductImage.get_image_absolute_url',
                 settings.ABSOLUTE_URL + '/media/image')

@pytest.fixture
def make_product_list_item():
    def _(products: list, product: int):
        return {
            'id': products[product].id,
            'name': products[product].name,
            'slug': settings.ABSOLUTE_URL
                    + '/api/v1/products/'
                    + products[product].slug,
            'thumbnail_url': settings.ABSOLUTE_URL + '/media/thumbnail',
            'marketing_price': str(products[product].marketing_price),
            'promotional_marketing_price': str(
                products[product].promotional_marketing_price)
        }
    return _

