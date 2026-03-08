from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm, CategoryForm, ProductImageForm

def create_category(request):
  if request.method == "POST":
    category_form = CategoryForm(request.POST)
    if category_form.is_valid():
      category_form.save()
      return redirect('create_product')
  category_form = CategoryForm()
  return render(request, 'products/category_form.html', {'category_form': category_form})

def create_product(request):
  if request.method == "POST":
    product_form = ProductForm(request.POST)
    if product_form.is_valid():
      product_form.save()
      return redirect('create_product')
  product_form = ProductForm()
  return render(request, 'products/product_form.html', {'product_form': product_form })

def add_images(request):
  """add multiple images for particular product"""
  # TODO: pending to add multiple images for particular product
  if request.method == "POST":
    product_image_form = ProductImageForm(request.FILES)
    if product_image_form.is_valid():
      product_image_form.save()
  product_image_form = ProductImageForm()
  return render(request, 'products/add_images.html', {'product_image_form': product_image_form})

def list_product(request):
  products = Product.objects.select_related('category').prefetch_related('product_image').all()
  return render(request, 'products/list_products.html', {'products':products})

def get_product(request, pk):
  product = get_object_or_404(Product.objects.select_related('category').prefetch_related('product_image'), id=pk)
  return render(request, 'products/product_details.html', {'product': product})

def edit_product(request, pk):
  product = get_object_or_404(Product, id=pk)
  if request.method == "POST":
    product_form = ProductForm(request.POST, instance=product)
    if product_form.is_valid():
      product_form.save()
      return redirect('product_list')
    else:
      print(product_form.errors)
  product_form = ProductForm(instance=product)
  return render(request, 'products/product_form.html', {'product_form':product_form})

def remove_product(request, pk):
  product = get_object_or_404(Product, id=pk)
  try:
    if request.method == "POST":
      product.delete()
    else:
      return redirect('list_product')
  except product.DoesNotExist:
    return redirect('list_product')