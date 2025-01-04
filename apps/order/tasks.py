from celery import shared_task

from .utils import send_order_confirmation_email
from .models import Order


@shared_task
def send_order_confirmation_email_async(order_id: str) -> None:
    order = Order.objects.get(id=order_id)
    send_order_confirmation_email(order)

