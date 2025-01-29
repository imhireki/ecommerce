from rest_framework import serializers

from . import models


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItem
        exclude = ["order"]


class OrderListSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    status = serializers.CharField(source="get_status_display", required=False)

    class Meta:
        model = models.Order
        exclude = ["user"]


class OrderCheckoutSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, write_only=True)
    status = serializers.CharField(source="get_status_display", required=False)

    class Meta:
        model = models.Order
        exclude = ["created_at"]
        extra_kwargs = {"status": {"write_only": True}, "user": {"write_only": True}}

    def create(self, validated_data):
        order_items = validated_data.pop("order_items")

        order_object = models.Order(**validated_data)
        order_object.save()

        for order_item in order_items:
            order_item_object = models.OrderItem(order=order_object, **order_item)
            order_item_object.save()

        return order_object
