from rest_framework import generics
from rest_framework import mixins

from . import serializers
from . import models


class ProductListView(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductDetailSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"


class ProductSearchView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = serializers.ProductListSerializer

    def get_queryset(self):
        return models.Product.objects.filter(
            name__icontains=self.request.data.get("query")
        )

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
