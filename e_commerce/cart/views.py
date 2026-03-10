from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem, Product
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def cart_view(request):
    """
     cart, create = if cart exist so get else create
     cart_item = fetch all cart item for particular cart
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.select_related("cart").filter(cart=cart)
    return render(
        request, "cart/cart_item.html", {"cart_items": cart_items, "cart": cart}
    )

@login_required(login_url='login')
def add_to_cart(request, pk):
    """
     pk = get product id 
     cart, create = if cart exist so get else create
     cart_item = create new cart item if not exist else increase quantity 
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=pk)
    cart_item, cart_item_created = CartItem.objects.get_or_create(
        product=product, cart=cart
    )

    if cart_item_created:
        return redirect('cart_view')

    if not cart_item_created:
        if product.stock > 0:
            cart_item.quantity += 1
            cart_item.save()
            return redirect("cart_view")
        else:
            print("product out of stock")

@login_required(login_url='login')
def remove_from_cart(request, pk):
    """
     pk = get product id 
     cart, create = if cart exist so get else create
     cart_item = remove cart item if exist while quantity > 1 else remove from cart
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=pk)
    cart_item = get_object_or_404(CartItem, product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        return redirect("cart_view")
    else:
        cart_item.delete()
        return redirect("cart_view")
