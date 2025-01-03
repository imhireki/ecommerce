import uuid

from django.conf import settings
from django.db import models


class Order(models.Model):
    ORDER_STATUS = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
        ('S', 'Sent'),
        ('F', 'Finalized'),
    ] 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=1,
                              choices=ORDER_STATUS,
                              default=ORDER_STATUS[0][0])
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return str(self.id)
            

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='order_items',
                              related_query_name='order_item')
    product = models.CharField(max_length=100)
    product_variation = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self) -> str:
        return f"Order {self.order.id}'s item"

