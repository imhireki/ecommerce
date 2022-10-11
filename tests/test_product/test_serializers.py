from django.conf import settings
from model_bakery import baker
import pytest

from apps.product import serializers


pytestmark = [pytest.mark.unit, pytest.mark.django_db]


class TestProductListSerializer:
    def test_serialize(self, mocker, patch_image):
        product = baker.make('product.Product')

        expected_data = {
            'id': product.id,
            'name': product.name,
            'slug': settings.ABSOLUTE_URL + '/api/v1/products/' + product.slug,
            'thumbnail_url': settings.ABSOLUTE_URL + '/media/thumbnail',
            'marketing_price': str(product.marketing_price),
            'promotional_marketing_price': str(
                product.promotional_marketing_price)
        }

        serializer = serializers.ProductListSerializer(product)

        assert serializer.data == expected_data


class TestProductImageSerializer:
    def test_serialize(self, mocker, patch_image):
        image = baker.make('product.ProductImage')

        mocker.patch.object(image.image, 'name', 'image')
        expected_data = {
            'id': image.id,
            'image_url': settings.ABSOLUTE_URL + image.image.url
        }

        serializer = serializers.ProductImageSerializer(image)

        assert serializer.data == expected_data


class TestProductVariationSerializer:
    def test_serialize(self, patch_image):
        variation = baker.make('product.ProductVariation')

        expected_data = {
            'id': variation.id,
            'name': variation.name,
            'quantity': variation.quantity,
            'price': variation.price,
            'promotional_price': variation.promotional_price
        }

        serializer = serializers.ProductVariationSerializer(variation)

        assert serializer.data == expected_data


class TestProductDetailSerializer:
    def test_serialize(self, mocker, patch_image):
        product = baker.make('product.Product')
        variation = baker.make('product.ProductVariation', product=product)
        image = baker.make('product.ProductImage', product=product)

        expected_data = {
            'name': product.name,
            'description': product.description,
            'images': [{
                'id': image.id,
                'image_url': settings.ABSOLUTE_URL + '/media/image'
            }],
            'variations': [{
                'id': variation.id,
                'name': variation.name,
                'quantity': variation.quantity,
                'price': variation.price,
                'promotional_price': variation.promotional_price
            }]
        }

        serializer = serializers.ProductDetailSerializer(product)

        assert serializer.data == expected_data

