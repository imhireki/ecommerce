from django.db.models.signals import post_save
from django.dispatch import receiver

from . import utils


@receiver(post_save, sender='order.Order')
def post_save_order(sender, instance, created, *args, **kwargs):
    if not created:
        return

    utils.send_order_confirmation_email(instance)

