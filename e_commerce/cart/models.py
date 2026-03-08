from django.db import models
import uuid
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Cart(models.Model):
  cart_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.user.username} - {self.cart_id}"
  
  @property
  def total(self):
    return sum(item.item_total for item in self.items.all())


class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
  quantity = models.PositiveIntegerField(default=1)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.cart.user.username} - {self.product.product_name} ({self.quantity})"
  
  @property
  def item_total(self):
    return self.product.price * self.quantity


