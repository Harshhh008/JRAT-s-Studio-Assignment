from django.contrib import admin
from .models import Order, OrderItem, Payment

class OrderItemInline(admin.TabularInline):
  model = OrderItem
  readonly_fields = (
    'orderitem_id','quantity', 'price'
  )
  extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  list_display = (
    'order_id', 'user__email', 'status', 'total_amount', 'created_at'
  )
  list_filter = ('status',)
  inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
  list_display = (
    'orderitem_id', 'order__order_id', 'order__user__email', 'order__status','order__payment__status', 'product__product_name', 'quantity', 'price', 'item_total'
  )
  search_fields = ('order__order_id', 'order__user__email', 'product__product_name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
  list_display = ('payment_id', 'order__order_id', 'payment_method', 'status', 'created_at')