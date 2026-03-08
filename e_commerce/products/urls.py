from django.urls import path
from . import views

urlpatterns = [
    path('category/create/', views.create_category, name='create_category'),
    path('create/', views.create_product, name='create_product'),
    path('add/image/', views.add_images, name='add_images'),
]
