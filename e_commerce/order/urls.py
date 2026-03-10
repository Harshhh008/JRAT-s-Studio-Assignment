from django.urls import path
from . import views

urlpatterns = [
  path('create/', views.create_order_from_cart, name='create_order'),
  path('check-out/<uuid:order_id>/', views.checkout_order, name='checkout_order'),
  path('check-out/payments/', views.payments, name='payments'),
  path('order-complete/', views.order_complete, name='order_complete'),
]
