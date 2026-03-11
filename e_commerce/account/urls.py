from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('edit-profile/<uuid:pk>/', views.edit_profile, name="edit_profile"),
    path('new/address/', views.add_address, name="add_address"),
    path('edit/address/<uuid:pk>/', views.edit_address, name="edit_address"),
    path('change-password/', views.change_password, name="change_password"),
    path('password-reset/', views.reset_password_view, name="reset_password"),
    path('password-reset/confirm/<str:user_id>/<str:token>/', views.reset_password_confirm_view, name="forgot_password_confirm"),
]