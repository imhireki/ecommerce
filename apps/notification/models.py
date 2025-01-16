from django.db import models


class Broadcast(models.Model):
    message = models.CharField(max_length=100)
    scheduled_to = models.DateTimeField()
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-scheduled_to']

    def __str__(self) -> str:
        return str(self.message)

