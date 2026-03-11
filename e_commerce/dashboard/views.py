from django.shortcuts import render
from products.models import Product
from order.models import OrderItem
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.db.models import Q

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
  q = request.GET.get('q', '')
  products = Product.objects.select_related('category').filter(product_name__icontains=q).order_by('-created_at')
  return render(request, 'dashboard/data.html', {'products': products})

def dashboard_users(request):
  q = request.GET.get('q', '')
  users = User.objects.prefetch_related('address').filter(Q(username__icontains=q) | Q(email__icontains=q)).order_by('-updated_at')
  return render(request, 'dashboard/data.html', {'users': users})

def dashboard_ordered_items(request):
  q =request.GET.get('q', '')
  order_items = OrderItem.objects.select_related('order', 'product', 'order__user', 'product__category', 'order__payment').prefetch_related('order__user__address').filter(Q(order__order_id__icontains=q) | Q(order__user__email=q))
  return render(request, 'dashboard/data.html', {'order_items': order_items})