from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from .models import Order
from django.conf import settings

def paypal_payment(request, order_id):
  order = Order.objects.get(order_id=order_id)
  paypal_dict = {
        "business":getattr(settings, "PAYPAL_RECEIVER_EMAIL"), 
        "amount": str(order.total_amount),
        "item_name": f"Order {order.order_id}",
        "invoice": str(order.order_id),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment_done')),
        "cancel_return": request.build_absolute_uri(reverse('payment_canceled')),
        "custom": str(order.user.id)
    }
  form = PayPalPaymentsForm(initial=paypal_dict)
  return render(request, 'order/payment.html', {'form': form})

  