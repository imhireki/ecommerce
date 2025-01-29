from celery import shared_task

from .models import Order
from . import utils


@shared_task
def send_order_confirmation_email_task(order_id: str) -> None:
    order = Order.objects.get(id=order_id)
    utils.send_order_confirmation_email(order)


@shared_task
def report_yesterday_orders_to_staff_email_task() -> None:
    utils.report_yesterday_orders_to_staff_email()
