from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
  list_display = (
    'cart_id', 'user__email', 'created_at', 'updated_at', 'total'
  )

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
  list_display = (
    'cart', 'product__product_name', 'quantity','created_at', 'updated_at', 'item_total'
  )
  search_fields = ('cart__user__email', 'product__product_name')