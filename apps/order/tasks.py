from celery import shared_task

from .models import Order
from . import utils


@shared_task
def send_order_confirmation_email_async(order_id: str) -> None:
    order = Order.objects.get(id=order_id)
    utils.send_order_confirmation_email(order)

