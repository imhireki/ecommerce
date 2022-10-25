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

