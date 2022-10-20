import uuid

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Order(models.Model):
    ORDER_STATUS = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
        ('S', 'Sent'),
        ('F', 'Finalized'),
    ] 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=1,
                              choices=ORDER_STATUS,
                              default=ORDER_STATUS[0][0])
    
    class Meta:
        ordering = ['-created_at']
            

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='order_items',
                              related_query_name='order_item')
    product = models.CharField(max_length=100)
    product_variation = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

