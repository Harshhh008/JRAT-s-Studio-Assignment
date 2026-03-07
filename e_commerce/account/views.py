from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm, AuthenticationForm

# Create your views here.
def user_register(request):
  """user register logic"""
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'registration successful.')
      return redirect('user_login')
    else:
      messages.error(request, 'something went wrong with registration')
  form = UserCreationForm()
  return render(request, 'account/register.html', {'form': form})

def user_login(request):
  """user login logic"""
  if request.method == "POST":
    form = AuthenticationForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data.get('email', None)
      password = form.cleaned_data.get('password', None)
      print(email, password)

      if not email and not password:
        messages.error(request, 'both fields are required')

      user = authenticate(email=email, password=password)
      print(user)

      if not user:
        messages.error(request, 'invalid email or password.')
        return redirect(f'user_login{request.user}')
      else:
        try:
          login(request ,user)
          return HttpResponse('home page after login')
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
    return redirect(login)