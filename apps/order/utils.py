from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from apps.order.models import Order, OrderItem


def send_order_confirmation_email(instance: Order):
    # Preload related User and OrderItem data
    order = (
        Order.objects.select_related('user')
        .prefetch_related('order_items').get(id=instance.id)
    )

    items = [
        f'{item.quantity}x product {item.product_variation} ${item.price}\n' 
        for item in OrderItem.objects.filter(order=order.id)
    ]

    subject = f'Order {order.id} at Django created'
    message=[
        f'Order {order.id} by {order.user.username}\n',
        f'Total: {order.paid_amount}\n',
        'Items:\n',
    ]
    message.extend(items)

    send_mail(subject, ''.join(message), None, [order.user.email])

def report_yesterday_orders_to_staff_email():
    yesterday = timezone.now() - timedelta(days=1)

    orders = (
        Order.objects.filter(created_at__date=yesterday)
        .prefetch_related('order_items')
    )
    items = OrderItem.objects.filter(order__in=orders)

    staff_members = [
        staff.email for staff in 
        get_user_model().objects.filter(is_staff=True)
    ]

    total = sum(order.paid_amount for order in orders)
    num_diff_users = len({order.user for order in orders})
    num_items = sum(item.quantity for item in items) 

    subject = 'Django report: ' + yesterday.date().strftime("%d/%m/%Y")
    message = [
        f'total: {total}\n',
        f'number of items: {num_items}\n',
        f'number of different users: {num_diff_users}',
    ]

    send_mail(subject, ''.join(message), None, recipient_list=staff_members)

