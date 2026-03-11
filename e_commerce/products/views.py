from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, ProductImage
from .forms import ProductForm, CategoryForm, ProductImageForm
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.decorators import permission_required, login_required


@permission_required("product.add_category")
@login_required(login_url='login')
def create_category(request):
    if request.method == "POST":
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect("create_product")
    category_form = CategoryForm()
    return render(
        request, "products/category_form.html", {"category_form": category_form}
    )

@permission_required("product.change_category")
@login_required(login_url='login')
def update_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == "POST":
        category_form = CategoryForm(request.POST, instance=category)
        category_form.save() if category_form.is_valid() else category_form.errors()
        return redirect('list_product')
    category_form = CategoryForm(instance=category)
    return render(request, 'products/category_form.html', {'category_form': category_form})

@permission_required("product.delete_category")
@login_required(login_url='login')
def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    try:
        product_exist = Category.objects.annotate(product_count = Count('product')).get(id=pk)
        if  product_exist.product_count > 0:
            print("You can not delete this category because product in this category is exist")
        else:
            category.delete()
    except Exception as e:
        print(str(e))
    return redirect('list_product')



@permission_required("product.add_product")
@login_required(login_url='login')
def create_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            return redirect("create_product")
    product_form = ProductForm()
    return render(request, "products/product_form.html", {"product_form": product_form})


def add_images(request, pk=None):
    """add multiple images for particular product"""
    product = get_object_or_404(Product, id=pk)
    if request.method == "POST":
        product_image_form = ProductImageForm(request.POST, request.FILES)
        if product_image_form.is_valid():
            image = product_image_form.save(commit=False)
            image.product = product
            image.save()
            return redirect('get_product', pk)
    product_image_form = ProductImageForm()
    return render(
        request, "products/add_images.html", {"product_image_form": product_image_form, 'product': product}
    )

def remove_images(request, p_pk=None, pk=None):
    """remove image"""
    image = ProductImage.objects.get(id=pk)
    image.delete()
    return redirect('get_product', p_pk)

def list_product(request, pk=None):
    category_name = None
    top_selling_products = None
    if pk:
        products = (
            Product.objects.select_related("category")
            .prefetch_related("product_image")
            .filter(category__id=pk).order_by('-created_at')
        )
        category_name = Category.objects.get(id=pk)
    else:
        products = (
            Product.objects.select_related("category")
            .prefetch_related("product_image")
            .order_by('-created_at')
        )
        top_selling_products = Product.objects.select_related('category').prefetch_related("product_image").order_by('-selling')[:5]
    return render(request, "products/list_products.html", {"products": products, "category_id": pk if pk else None, "category_name": category_name, "top_selling_products": top_selling_products})


def get_product(request, pk):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("product_image"),
        id=pk,
    )
    return render(request, "products/product_details.html", {"product": product})


@permission_required("product.change_product")
@login_required(login_url='login')
def edit_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == "POST":
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect("list_product")
        else:
            print(product_form.errors)
    product_form = ProductForm(instance=product)
    return render(request, "products/product_form.html", {"product_form": product_form})


@permission_required("product.delete_product")
@login_required(login_url='login')
def remove_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == "POST":
        product.delete()
        return redirect("list_product")
    return render(request, 'products/remove_product.html', {'product': product})

def search_product(request):
    q = request.GET.get('q')
    products = Product.objects.select_related('category').filter(
        Q(product_name__icontains=q) |
        Q(category__category_name__icontains=q) 
    )
    return render(request, 'products/list_products.html', {'products': products})
