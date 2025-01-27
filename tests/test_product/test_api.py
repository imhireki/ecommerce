import json

from model_bakery import baker
import pytest


pytestmark = [pytest.mark.django_db, pytest.mark.integration]


class TestProductEndpoints:
    endpoint = "/api/v1/products/"

    def test_list_products(self, api_client, patch_image, get_product_list_data):
        products = baker.make("product.Product", 2)

        response = api_client().get(self.endpoint)

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 2
        assert get_product_list_data(products[0]) and get_product_list_data(
            products[1]
        ) in json.loads(response.content)

    def test_retrieve_product(self, api_client, patch_image, get_product_detail_data):
        product = baker.make("product.Product")
        variations = baker.make("product.ProductVariation", 2, product=product)
        images = baker.make("product.ProductImage", 5, product=product)

        response = api_client().get(f"{self.endpoint}{product.slug}/")

        assert response.status_code == 200
        assert json.loads(response.content) == get_product_detail_data(
            product, images, variations
        )

    def test_search_products(self, api_client, patch_image, get_product_list_data):
        products = baker.make("product.Product", 3)

        response = api_client().post(
            self.endpoint + "search/", {"query": products[0].name}, format="json"
        )

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1
        assert get_product_list_data(products[0]) in json.loads(response.content)
