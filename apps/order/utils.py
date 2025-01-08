from datetime import timedelta

from django.template.loader import render_to_string
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

    context = {
        'username': order.user.username,
        'total': order.paid_amount,
        'order': order.id,
        'items': list(OrderItem.objects.filter(order=order.id))
    }

    email = render_to_string('emails/order_confirmation_email.html', context)
    subject = '[E-commerce] Confirmed order'

    send_mail(subject, '', None, [order.user.email], html_message=email)

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

    date = yesterday.date().strftime("%d/%m/%Y")
    total = sum(order.paid_amount for order in orders)
    num_diff_users = len({order.user for order in orders})
    num_items = sum(item.quantity for item in items) 

    context = {
        'date': date,
        'total': total,
        'num_items': num_items,
        'num_diff_users': num_diff_users,
    }
    subject = '[E-commerce] ' + date + ' report'

    email = render_to_string('emails/daily_report.html', context)

    send_mail(subject, '', None, staff_members, html_message=email)

