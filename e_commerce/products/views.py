from django.shortcuts import render, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm, ProductImageForm

def create_category(request):
  if request.method == "POST":
    category_form = CategoryForm(request.POST)
    if category_form.is_valid():
      category_form.save()
      return redirect('create_product')
  category_form = CategoryForm()
  return render(request, 'products/create_category.html', {'category_form': category_form})

def create_product(request):
  if request.method == "POST":
    product_form = ProductForm(request.POST)
    if product_form.is_valid():
      product_form.save()
      return redirect('create_product')
  product_form = ProductForm()
  return render(request, 'products/create_product.html', {'product_form': product_form })

def add_images(request):
  """add multiple images for particular product"""
  # TODO: pending to add multiple images for particular product
  if request.method == "POST":
    product_image_form = ProductImageForm(request.FILES)
    if product_image_form.is_valid():
      product_image_form.save()
  product_image_form = ProductImageForm()
  return render(request, 'products/add_images.html', {'product_image_form': product_image_form})