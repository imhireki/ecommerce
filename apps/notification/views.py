from rest_framework import generics
from django.utils import timezone

from . import serializers
from . import models


class BroadcastListView(generics.ListAPIView):
    serializer_class = serializers.BroadcastSerializer

    def get_queryset(self):
        # Exclude broadcasts after current date
        return models.Broadcast.objects.filter(scheduled_to__lt=timezone.now())
