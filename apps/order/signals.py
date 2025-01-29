from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import send_order_confirmation_email_task


@receiver(post_save, sender="order.Order")
def post_save_order(sender, instance, created, *args, **kwargs):
    if not created:
        return

    send_order_confirmation_email_task.delay(str(instance.id))
