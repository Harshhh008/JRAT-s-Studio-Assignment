from django.shortcuts import redirect, render
from cart.models import CartItem, Cart
from .models import Order, OrderItem, Payment
import json
from django.http import JsonResponse
from account.models import UserAddress
from utils.email import purchase_success_email
from django.contrib.auth.decorators import login_required

login_required(login_url='login')
def create_order_from_cart(request):
  cart = Cart.objects.get(user=request.user)
  address = UserAddress.objects.filter(user=request.user).first().full_address

  order = Order.objects.create(
    user = request.user,
    shipping_address=address,
    total_amount = cart.total,
    status="pending"
  )
  return redirect('checkout_order', order_id=order.order_id)

login_required(login_url='login')
def checkout_order(request, order_id):
  order = Order.objects.get(order_id=order_id)
  return render(request, 'order/checkout.html', {'order_id': order_id, 'total_amount': order.total_amount})
  
login_required(login_url='login')
def payments(request):
  body = json.loads(request.body)
  order = Order.objects.get(order_id=body['orderID'])
  cart = Cart.objects.get(user=request.user)
  cart_item = CartItem.objects.select_related('product').filter(cart=cart)

  if len(cart_item) <= 0:
    return redirect('list_product')
  # store payment data
  # print(body)
  # print(body['status'].title())
  payment, created = Payment.objects.get_or_create(
    paypal_payment_id = body['transID'],
    order = order,
    payment_method = body['payment_method'],
    status=body['status'].lower()
  )

  if not created:
    payment.paypal_payment_id = body['transID']
    payment.status = body['status'].lower()
    payment.save()
  order.status = "processing"
  order.save()

  for item in cart_item:
    OrderItem.objects.create(
      order=order,
      product = item.product,
      quantity = item.quantity,
      price = item.product.price
  )
    # reduce product stock after order item create
    product = item.product
    product.stock -= item.quantity
    product.selling += item.quantity
    product.save()
    
  # remove all cart item after payment
  cart = Cart.objects.get(user=request.user)
  CartItem.objects.filter(cart=cart).delete()

  # send back json data to frontend
  data = {
    'orderID': order.order_id, 
    'transID': payment.payment_id
  }  

  return JsonResponse(data)

login_required(login_url='login')
def order_complete(request):
  order_id = request.GET.get('order_number')
  payment_id = request.GET.get('payment_id')
  order_items = None
  try:
    # get all ordered data
    order = Order.objects.get(order_id=order_id)
    order_items = OrderItem.objects.select_related('product').filter(order=order)

    #send email
    purchase_success_email(request.user.email)
  except Exception as e:
    print(str(e))
  return render(request, 'order/order-complete.html', {'order_items': order_items,'order_id': order_id, 'payment_id': payment_id})
    