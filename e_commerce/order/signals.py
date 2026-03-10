from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.db import transaction
from cart.models import CartItem
from .models import Order, OrderItem

def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Payment successful
        try:
            order = Order.objects.get(order_id=ipn_obj.invoice)
            if order.status != "completed":
                cart_items = CartItem.objects.select_related('product').filter(cart__user=order.user)

                with transaction.atomic():
                    # Reduce stock
                    for item in cart_items:
                        product = item.product
                        if product.stock < item.quantity:
                            raise ValueError(f"{product.product_name} out of stock")
                        product.stock -= item.quantity
                        product.save()

                    # Delete cart items
                    cart_items.delete()

                    # Mark order as completed
                    order.status = "completed"
                    order.save()
        except Order.DoesNotExist:
            pass

valid_ipn_received.connect(payment_notification)