from rest_framework import serializers

from .models import Broadcast


class BroadcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broadcast
        exclude = ['scheduled_to']

