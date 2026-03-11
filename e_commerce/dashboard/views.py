from django.shortcuts import render
from products.models import Product
from order.models import OrderItem
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model

User = get_user_model()

def staff_or_admin(user):
  return user.is_staff or user.is_superuser


@login_required(login_url='login')
@user_passes_test(staff_or_admin, login_url='login')
def dashboard(request):
  return render(request, 'dashboard/dashboard.html')


def dashboard_categories(request):
  return render(request, 'dashboard/data.html')

def dashboard_products(request):
  products = Product.objects.select_related('category').all()
  return render(request, 'dashboard/data.html', {'products': products})

def dashboard_users(request):
  users = User.objects.prefetch_related('address').all()
  return render(request, 'dashboard/data.html', {'users': users})

def dashboard_ordered_items(request):
  order_items = OrderItem.objects.select_related('order', 'product', 'order__user', 'product__category', 'order__payment').prefetch_related('order__user__address').all()
  return render(request, 'dashboard/data.html', {'order_items': order_items})