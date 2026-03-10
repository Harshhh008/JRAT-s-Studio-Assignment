from django.db import models
from django.contrib.auth import get_user_model
import uuid
from products.models import Product

User = get_user_model()

class Order(models.Model):
    ORDER_STATUS = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    status = models.CharField(max_length=220, choices=ORDER_STATUS, default="pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return f"Order {self.order_id}"

class OrderItem(models.Model):
    orderitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_item")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
      return f"{self.product.product_name} ({self.quantity})"
    
    @property
    def item_total(self):
      return self.price * self.quantity
    
class Payment(models.Model):
    PAYMENT_STATUS = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    )
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    payment_method = models.CharField(max_length=40)
    paypal_payment_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
      max_length=20,
      choices=PAYMENT_STATUS,
      default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return f"Payment for Order {self.order.order_id}"

  
  