from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_product, name="list_product"),
    # create urls
    path("category/create/", views.create_category, name="create_category"),
    path("create/", views.create_product, name="create_product"),
    path("add/image/", views.add_images, name="add_images"),

    path("", views.add_images, name="add_images"),
    path('<uuid:pk>/', views.get_product, name="get_product"),
    # update
    path("edit/<uuid:pk>/", views.edit_product, name="edit_product"),
    # delete
    path("delete/<uuid:pk>/", views.remove_product, name="remove_product")
]
