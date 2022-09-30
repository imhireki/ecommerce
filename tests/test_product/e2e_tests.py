import json

from django.conf import settings
from model_bakery import baker
import pytest


pytestmark = [pytest.mark.django_db, pytest.mark.e2e]

@pytest.fixture(autouse=True)
def patch_resize_image(mocker):
    mocker.patch('apps.product.utils.resize_image', lambda image, size: image)


class TestProductEndpoints:
    endpoint = '/api/v1/products/'

    def test_list_products(self, api_client, mocker):
        def get_expected_data(products: list, product: int):
            return {
                'id': products[product].id,
                'name': products[product].name,
                'slug': settings.ABSOLUTE_URL + '/' + products[product].slug,
                'thumbnail_url': settings.ABSOLUTE_URL + '/media/thumbnail',
                'marketing_price': products[product].marketing_price,
                'promotional_marketing_price': products[product].
                                               promotional_marketing_price
            }
        mocker.patch('apps.product.models.Product.get_thumbnail_absolute_url',
                     settings.ABSOLUTE_URL + '/media/thumbnail')
        products = baker.make('product.Product', 2)

        response = api_client().get(self.endpoint)
        
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2
        assert json.loads(response.content)[0] == get_expected_data(products, 0)
        assert json.loads(response.content)[1] == get_expected_data(products, 1)

    def test_retrieve_product(self, api_client):
        product = baker.make('product.Product')
        variations = baker.make('product.ProductVariation', 2, product=product)
        images = baker.make('product.ProductImage', 3, product=product)
        
        expected_json = {
            "name": product.name,
            "description": product.description,
            "images": [{
                'id': image.id,
                'image_url': settings.ABSOLUTE_URL + '/media/image'
            } for image in images],
            "variations": [{
                "id": variation.id,
                "name": variation.name,
                "quantity": variation.quantity,
                "price": variation.price,
                "promotional_price": variation.promotional_price,
            } for variation in variations]
        }
         
        response = api_client().get(f'{self.endpoint}{product.slug}/')

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_search_products(self, api_client):
        baker.make('product.Product', name='name')

        response = api_client().get(f'{self.endpoint}?search=name')

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

