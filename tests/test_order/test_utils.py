from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.core import mail
from model_bakery import baker
import pytest

from apps.order import models
from apps.order import utils


pytestmark = [pytest.mark.django_db, pytest.mark.unit]

def test_send_order_confirmation_email(mocker):
    order = baker.make('order.Order', user__email='t1@ex.com')
    baker.make('order.OrderItem', 2, order=order)

    rts = mocker.patch('apps.order.utils.render_to_string',
                       return_value='<html>email</html>')

    utils.send_order_confirmation_email(order)

    context = {
        'username': order.user.username,
        'total': order.paid_amount,
        'order': order.id,
        'items': list(models.OrderItem.objects.filter(order=order.id))
    }

    assert rts.call_args[0][0] == 'emails/order_confirmation_email.html'
    assert rts.call_args[0][1] == context 
    assert mail.outbox[0].to == [order.user.email]
    assert mail.outbox[0].from_email == settings.DEFAULT_FROM_EMAIL
    assert mail.outbox[0].subject == '[E-commerce] Confirmed order'
    assert mail.outbox[0].alternatives[0][0] == '<html>email</html>'

def test_report_yesterday_orders_to_staff_email(mocker):
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

    rts = mocker.patch('apps.order.utils.render_to_string',
                       return_value='<html>email</html>')

    utils.report_yesterday_orders_to_staff_email()

    date = yesterday.date().strftime("%d/%m/%Y")
    context = {
        'date': date,
        'total': 20.00,
        'num_items': 8,
        'num_diff_users': 3,
    }

    assert rts.call_args[0][0] == 'emails/daily_report.html'
    assert rts.call_args[0][1] == context 
    assert mail.outbox[0].to == ['t1@ex.com', 't2@ex.com']
    assert mail.outbox[0].from_email == settings.DEFAULT_FROM_EMAIL
    assert mail.outbox[0].subject == '[E-commerce] ' + date + ' report'
    assert mail.outbox[0].alternatives[0][0] == '<html>email</html>'

