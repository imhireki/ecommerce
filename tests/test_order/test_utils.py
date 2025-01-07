from django.test import override_settings
from django.conf import settings
from model_bakery import baker
from django.core import mail
import pytest

from apps.order import utils


pytestmark = [pytest.mark.django_db, pytest.mark.unit]

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
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

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [order.user.email]
    assert mail.outbox[0].from_email == settings.DEFAULT_FROM_EMAIL
    assert mail.outbox[0].subject == subject
    assert mail.outbox[0].body == ''.join(message)

