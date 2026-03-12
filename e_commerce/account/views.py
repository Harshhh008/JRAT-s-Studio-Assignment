from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import UserAddress
from order.models import Order

from .forms import UserCreationForm, AuthenticationForm, UserProfileForm, UserAddressForm, ForgotPasswordForm
from utils.email import send_reset_password_email

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm

User = get_user_model()


# Create your views here.
def user_register(request):
  """user register logic"""
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
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
          messages.success(request, 'logged in successfully.')
          if next_url:
            return redirect(next_url)
          else:
            return redirect('list_product')
        except Exception as e:
          print(str(e))
    else:
      messages.error(request, "something went wrong.")
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
    messages.success(request, "you have logged out successfully.")
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
      messages.success(request, "Your profile is updated.")
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
      messages.success(request, 'New address added successfully.')
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
      messages.success(request, 'Your address updated successfully.')
      return redirect('profile')
  address_form = UserAddressForm(instance=address)
  return render(request, 'account/address_form.html', {'address_form': address_form})


def reset_password_view(request):
  if request.method == "POST":
    form = ForgotPasswordForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data.get('email')
      user = User.objects.filter(email=email).first()
      if user:
        # encode id
        user_id = urlsafe_base64_encode(force_bytes(user.id))
        token = default_token_generator.make_token(user)

        reset_password_link = reverse(
            "forgot_password_confirm", kwargs={"user_id": user_id, "token": token} 
        )
        reset_password_email_link = f"{request.build_absolute_uri(reset_password_link)}"
        send_reset_password_email(email, reset_password_email_link)
        messages.success(request, f'reset link sended your email {email}')

  form = ForgotPasswordForm()
  return render(request, 'account/reset_password.html', {'form': form})

def reset_password_confirm_view(request, user_id, token):
  user_id = force_str(urlsafe_base64_decode(user_id))
  user = User.objects.get(id=user_id)
  token = default_token_generator.check_token(user, token)
  if not token:
    messages.error(request, "This link expired or invalid.")
    return redirect('reset_password')
  else:
    if request.method == "POST":
      form = SetPasswordForm(user, request.POST)
      if form.is_valid():
        form.save()
        logout(request)
        messages.success(request, "Your password changed successfully.")
        return redirect('login')
      else:
        print(form.errors)
    form = SetPasswordForm(user)
    return render(request, 'account/reset_password_confirm.html', {'form': form})

@login_required(login_url='login')
def change_password(request):
  if request.method == "POST":
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
      try:
        form.save()
        logout(request)
        messages.success(request, 'password changed successfully now you can login with your new password!')
        return redirect('login')
      except Exception as e:
        print(str(e))
    else:
      messages.error(request, "Something wrong. Please try again.")
  form = PasswordChangeForm(user=request.user)
  return render(request, 'account/password_change.html', {'form': form})