import json

from django.conf import settings
from model_bakery import baker
import pytest


pytestmark = [pytest.mark.django_db, pytest.mark.e2e]


class TestProductEndpoints:
    endpoint = '/api/v1/products/'

    def test_list_products(self, api_client, make_product_list_item, patch_image):
        products = baker.make('product.Product', 2)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2
        assert make_product_list_item(products, 0) \
               and make_product_list_item(products, 1) \
               in json.loads(response.content)

    def test_retrieve_product(self, api_client, patch_image):
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

    def test_search_products(self, api_client, make_product_list_item, patch_image):
        product = baker.make('product.Product', name='name')

        response = api_client().post(
            self.endpoint + 'search/',
            {"query": product.name},
            format='json')

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1
        assert make_product_list_item([product], 0) \
               in json.loads(response.content)

