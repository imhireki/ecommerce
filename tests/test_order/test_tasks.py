from model_bakery import baker
import pytest

from apps.order import tasks


pytestmark = [pytest.mark.unit, pytest.mark.celery]


@pytest.mark.django_db(transaction=True)
def test_send_order_confirmation_email_task(celery_session_worker, mocker):
    send_email = mocker.patch("apps.order.utils.send_order_confirmation_email")

    order = baker.make("order.Order")

    tasks.send_order_confirmation_email_task.delay(str(order.id)).get(timeout=5)

    send_email.assert_called_with(order)


def test_report_yesterday_orders_to_staff_email_task(celery_session_worker, mocker):
    report = mocker.patch("apps.order.utils.report_yesterday_orders_to_staff_email")

    tasks.report_yesterday_orders_to_staff_email_task()

    report.assert_called()
