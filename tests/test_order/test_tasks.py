from model_bakery import baker
import pytest

from apps.order import tasks


pytestmark = [pytest.mark.unit, pytest.mark.celery]

@pytest.mark.django_db(transaction=True)
def test_send_order_confirmation_email_async(celery_session_worker, mocker):
    send_email = mocker.patch('apps.order.tasks.send_order_confirmation_email') 

    order = baker.make('order.Order')

    tasks.send_order_confirmation_email_async.delay(str(order.id)).get(timeout=5)

    assert send_email.called
    assert send_email.call_args.args[0] == order

