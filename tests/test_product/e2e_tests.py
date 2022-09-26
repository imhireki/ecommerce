import json

from model_bakery import baker
import pytest


pytestmark = [pytest.mark.django_db, pytest.mark.e2e]


class TestProductEndpoints:
    endpoint = '/api/v1/products/'

    def test_list_products(self, api_client):
        baker.make('product.Product', 3)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve_product(self, api_client, mocker):
        mocker.patch('apps.product.utils.resize_image',
                     lambda original_image, size: original_image)
        product = baker.make('product.Product')
        variations = baker.make('product.ProductVariation', 2, product=product)
        images = baker.make('product.ProductImage', 3, product=product)
        
        expected_variations = [
            {
            "name": variation.name, "price": variation.price,
            "promotional_price": variation.promotional_price
            }
            for variation in variations
        ]

        expected_json = {
            "name": product.name,
            "description": product.description,
            "marketing_price": product.marketing_price,
            "promotional_marketing_price": product.promotional_marketing_price,
            "images": [image.image for image in images],
            "variations": expected_variations
        }
         
        response = api_client().get(f'{self.endpoint}{product.slug}/')

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    def test_search_products(self, api_client):
        product_name = 'xyz'
        baker.make('product.Product', name=product_name)

        response = api_client().get(f'{self.endpoint}?search={product_name}')

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

