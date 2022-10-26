from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from . import serializers
from . import models


class OrderCheckoutView(generics.CreateAPIView):
    serializer_class = serializers.OrderCheckoutSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        order_items = request.data.get('order_items')

        request.data.update({
            "user": request.user.id,
            "order_items": order_items,
            "paid_amount": sum([
                product_variation['price']
                for product_variation in order_items 
            ])
        })
        
        return super().create(request, *args, **kwargs)

class OrderListView(generics.ListAPIView):
    serializer_class = serializers.OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Order.objects.filter(user=self.request.user)

