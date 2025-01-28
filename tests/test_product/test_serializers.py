from model_bakery import baker
import pytest

from apps.product import serializers


pytestmark = [pytest.mark.unit, pytest.mark.django_db]


class TestProductListSerializer:
    def test_serialize(self, patch_image, get_product_list_data):
        product = baker.make("product.Product")
        serializer = serializers.ProductListSerializer(product)

        assert serializer.data == get_product_list_data(product)


class TestProductImageSerializer:
    def test_serialize(self, mocker, patch_image, get_product_image_data):
        image = baker.make("product.ProductImage")
        serializer = serializers.ProductImageSerializer(image)

        assert serializer.data == get_product_image_data(image)


class TestProductVariationSerializer:
    def test_serialize(self, patch_image, get_product_variation_data):
        variation = baker.make("product.ProductVariation")
        serializer = serializers.ProductVariationSerializer(variation)

        assert serializer.data == get_product_variation_data(variation)


class TestProductDetailSerializer:
    def test_serialize(self, patch_image, get_product_detail_data):
        product = baker.make("product.Product")
        variation = baker.make("product.ProductVariation", 2, product=product)
        image = baker.make("product.ProductImage", 3, product=product)

        serializer = serializers.ProductDetailSerializer(product)

        assert serializer.data == get_product_detail_data(product, image, variation)
