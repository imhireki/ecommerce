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
def get_product_list_data():
    return lambda product: {
        'id': product.id,
        'name': product.name,
        'slug': settings.ABSOLUTE_URL + '/api/v1/products/' + product.slug,
        'thumbnail_url': settings.ABSOLUTE_URL + '/media/thumbnail',
        'marketing_price': str(product.marketing_price),
        'promotional_marketing_price': str(
            product.promotional_marketing_price)
        }

@pytest.fixture
def get_product_detail_data(get_product_image_data,
                            get_product_variation_data):
    return lambda product, images, variations: {
        'name': product.name,
        'description': product.description,
        'images': [get_product_image_data(image) for image in images],
        'variations': [
            get_product_variation_data(variation)
            for variation in variations
        ]}

@pytest.fixture
def get_product_image_data():
    return lambda image: {
        'id': image.id,
        'image_url': settings.ABSOLUTE_URL + '/media/image'
        }

@pytest.fixture
def get_product_variation_data():
    return lambda variation: {
        'id': variation.id,
        'name': variation.name,
        'quantity': variation.quantity,
        'price': variation.price,
        'promotional_price': variation.promotional_price
        }

