from django.urls import path
from . import views

urlpatterns = [
  path('items/', views.cart_view, name="cart_view"),
  path('items/add/<uuid:pk>/', views.add_to_cart, name="add_to_cart"),
  path('items/remove/<uuid:pk>/', views.remove_from_cart, name="remove_from_cart"),
]