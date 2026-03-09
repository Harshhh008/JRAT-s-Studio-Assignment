from django.urls import path
from . import views

urlpatterns = [
    # category operations
    path("category/create/", views.create_category, name="create_category"),
    path('category/edit/<uuid:pk>/', views.update_category, name="category_update"),
    path('category/remove/<uuid:pk>/', views.delete_category, name="category_delete"),
    # list products
    path("", views.list_product, name="list_product"),
    path("category/<uuid:pk>/", views.list_product, name="list_by_category"),

    # create urls
    path("create/", views.create_product, name="create_product"),
    # add and remove images
    path("add/image/<uuid:pk>/", views.add_images, name="add_images"),
    path("remove/image/<uuid:p_pk>/<uuid:pk>/", views.remove_images, name="remove_images"),

    path("", views.add_images, name="add_images"),
    path('get_product/<uuid:pk>/', views.get_product, name="get_product"),
    # update product
    path("edit/<uuid:pk>/", views.edit_product, name="edit_product"),
    # delete product
    path("delete/<uuid:pk>/", views.remove_product, name="remove_product"),

    # search product
    path('search/', views.search_product, name='search_product')
]
