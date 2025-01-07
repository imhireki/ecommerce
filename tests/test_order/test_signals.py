from django.db.models.signals import post_save
from model_bakery import baker
import pytest

from apps.order.models import Order


pytestmark = [pytest.mark.django_db, pytest.mark.unit]


@pytest.mark.parametrize('creating, send_email',
                         [(True, True), (False, False)])
def test_post_save_order(mocker, creating, send_email,
                         enable_post_save_signal):
    send_email_mock = mocker.patch(
        'apps.order.signals.send_order_confirmation_email_async.delay')
    order = baker.prepare('order.Order')

    post_save.send(Order, instance=order, created=creating)

    assert send_email_mock.called == send_email
    
