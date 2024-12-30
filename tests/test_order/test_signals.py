from django.db.models.signals import post_save
from model_bakery import baker
import pytest

from apps.order.models import Order


pytestmark = [pytest.mark.django_db, pytest.mark.unit]


@pytest.mark.parametrize('created, expect_email', 
                         [(True, True), (False, False)])
def test_post_save_order(mocker, created, expect_email):
    send_email_mock = mocker.patch(
        'apps.order.signals.utils.send_order_confirmation_email')
    order = baker.prepare('order.Order')

    post_save.send(Order, instance=order, created=created)

    assert send_email_mock.called == expect_email
    
