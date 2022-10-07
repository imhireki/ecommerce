from rest_framework import serializers

from .models import Product, ProductImage, ProductVariation


class ProductListSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(source='get_slug_absolute_url')
    thumbnail_url = serializers.CharField(source='get_thumbnail_absolute_url')

    class Meta:
        model = Product
        exclude = ['description', 'thumbnail']


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(source='get_image_absolute_url')

    class Meta:
        model = ProductImage
        exclude = ['product', 'image']


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        exclude = ['product']


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    variations = ProductVariationSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'images', 'variations']

