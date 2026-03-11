from django.urls import path
from . import views

urlpatterns = [
    path("main/", views.dashboard, name="dashboard_main"),
    path("main/categories/", views.dashboard_categories, name="dashboard_categories"),
    path("main/products/", views.dashboard_products, name="dashboard_products"),
    path("main/users/", views.dashboard_users, name="dashboard_users"),
]
