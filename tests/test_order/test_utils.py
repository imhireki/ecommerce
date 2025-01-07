from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core import mail
from model_bakery import baker
import pytest

from apps.order import utils


pytestmark = [pytest.mark.django_db, pytest.mark.unit]

def test_send_order_confirmation_email():
    order = baker.make('order.Order', user__email='test@email.com')
    items = baker.make('order.OrderItem', 2, order=order)

    utils.send_order_confirmation_email(order)
    subject = f'Order {order.id} at Django created'
    message=[
        f'Order {order.id} by {order.user.username}\n',
        f'Total: {order.paid_amount}\n',
        'Items:\n',
        f'{items[0].quantity}x product {items[0].product_variation} ${items[0].price}\n',
        f'{items[1].quantity}x product {items[1].product_variation} ${items[1].price}\n'
    ]

    assert mail.outbox[0].to == [order.user.email]
    assert mail.outbox[0].from_email == settings.DEFAULT_FROM_EMAIL
    assert mail.outbox[0].subject == subject
    assert mail.outbox[0].body == ''.join(message)

def test_report_yesterday_orders_to_staff_email():
    yesterday = timezone.now() - timedelta(days=1)

    user = baker.make('User')
    orders_w_items = baker.make('order.Order', 2, created_at=yesterday,
                                paid_amount=5)
    orders_w_same_user = baker.make('order.Order', 2, created_at=yesterday,
                                    paid_amount=5, user=user)

    # 8 order items for yesterday
    baker.make('order.OrderItem', 2, order=orders_w_items[0])
    baker.make('order.OrderItem', 2, order=orders_w_items[1])
    baker.make('order.OrderItem', 2, order=orders_w_same_user[0])
    baker.make('order.OrderItem', 2, order=orders_w_same_user[1])
    # staff
    baker.make('User', 1, is_staff=True, email='t1@ex.com')
    baker.make('User', 1, is_staff=True, email='t2@ex.com')

    # noise
    baker.make('order.Order', 1, created_at=timezone.now())
    baker.make('order.Order', 3, created_at=timezone.now() - timedelta(days=2))
    baker.make('order.OrderItem', 2)

    utils.report_yesterday_orders_to_staff_email()

    subject = 'Django report: ' + yesterday.date().strftime("%d/%m/%Y")
    message = [
        'total: 20.00\n',
        'number of items: 8\n',
        'number of different users: 3',
    ]

    assert mail.outbox[0].to == ['t1@ex.com', 't2@ex.com']
    assert mail.outbox[0].from_email == settings.DEFAULT_FROM_EMAIL
    assert mail.outbox[0].subject == subject
    assert mail.outbox[0].body == ''.join(message)
