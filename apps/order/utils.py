from django.core.mail import send_mail

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

