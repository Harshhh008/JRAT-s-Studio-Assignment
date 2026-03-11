from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from .models import UserAddress
from order.models import Order
from products.models import Product, Category

from .forms import UserCreationForm, AuthenticationForm, UserProfileForm, UserAddressForm

User = get_user_model()


# Create your views here.
def user_register(request):
  """user register logic"""
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      # BUG: fixed is_active = True | default = False
      user.is_active = True
      user.save()
      messages.success(request, 'registration successful.')
      return redirect('login')
    else:
      messages.error(request, 'something went wrong with registration')
  form = UserCreationForm()
  return render(request, 'account/register.html', {'form': form})

def user_login(request):
  """user login logic"""

  # capture perticuler url if we not logged in
  next_url = request.GET.get('next')

  if request.method == "POST":
    form = AuthenticationForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data.get('email', None)
      password = form.cleaned_data.get('password', None)

      if not email and not password:
        messages.error(request, 'both fields are required')

      try:
        user = authenticate(email=email, password=password)

      except Exception as e:
        print(str(e))
      if not user:
        messages.error(request, 'invalid email or password.')
        return redirect('login')
      else:
        try:
          login(request ,user)
          if next_url:
            print("next working)")
            return redirect(next_url)
          else:
            print("working")
            return redirect('list_product')
        except Exception as e:
          print(str(e))
    else:
      print(form.errors)
  form = AuthenticationForm()
  return render(request, 'account/login.html', {'form': form})

@login_required(login_url='login')
def user_logout(request):
  """user logout logic"""
  try:
    logout(request)
  except Exception as e:
    print(str(e))
  else:
    return redirect('login')

@login_required(login_url='login')
def profile(request):
  # addresses
  user_addresses = UserAddress.objects.filter(user=request.user)
  # user all orders
  orders = Order.objects.prefetch_related('order_item','order_item__product', 'payment').filter(user=request.user).order_by('-created_at')

  return render(request, 'account/profile.html', {'user': request.user, 'user_addresses': user_addresses, 'orders': orders})

@login_required(login_url='login')
def edit_profile(request, pk):
  user = User.objects.get(id=pk)
  if request.method == "POST":
    profile_form = UserProfileForm(request.POST, instance=user)
    if profile_form.is_valid():
      data = profile_form.save(commit=False)
      data.user = request.user
      data.save()
      return redirect('profile')
  profile_form = UserProfileForm(instance=user)
  return render(request, 'account/profile_edit.html', {'profile_form': profile_form})

def add_address(request):
  if request.method == 'POST':
    address_form = UserAddressForm(request.POST)
    if address_form.is_valid():
      data = address_form.save(commit=False)
      data.user = request.user
      data.save()
      return redirect('profile')

  address_form = UserAddressForm()
  return render(request, 'account/address_form.html', {'address_form': address_form})

def edit_address(request, pk):
  address = UserAddress.objects.get(id=pk)
  if request.method == 'POST':
    address_form = UserAddressForm(request.POST, instance=address)
    if address_form.is_valid():
      data = address_form.save(commit=False)
      data.user = request.user
      data.save()
      return redirect('profile')
  address_form = UserAddressForm(instance=address)
  return render(request, 'account/address_form.html', {'address_form': address_form})