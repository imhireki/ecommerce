from rest_framework.response import Response
from rest_framework import generics

from .serializers import ProductListSerializer, ProductDetailSerializer
from .models import Product


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class ProductSearchView(generics.GenericAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.query)

    def post(self, request):
        self.query = request.data.get('query')

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
