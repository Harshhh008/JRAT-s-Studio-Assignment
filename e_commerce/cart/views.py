from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem, Product
from django.contrib.auth.decorators import login_required


def cart_view(request):
    """
     cart, create = if cart exist so get else create
     cart_item = fetch all cart item for particular cart
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.select_related("cart").filter(cart=cart)
        return render(
            request, "cart/cart_item.html", {"cart_items": cart_items, "cart": cart}
        )
    else:
        session_cart = request.session.get("cart", {})
        cart_items = []

        for pid, item in session_cart.items():
            product = get_object_or_404(Product, id=pid)
            cart_items.append({
                "product": product,
                "quantity": item["quantity"],
                "price": item["price"]
            })

        return render(request, "cart/cart_item.html", {"cart_items": cart_items})

def add_to_cart(request, pk):
    """
     pk = get product id 
     cart, create = if cart exist so get else create
     cart_item = create new cart item if not exist else increase quantity 
     session based cart if user is not logged  in still cart works
    """
    product = get_object_or_404(Product, id=pk)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
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
    else:
        # guest cart
        cart = request.session.get('cart', {})

        product_id = str(product.id)

        if product_id in cart:
            cart[product_id]['quantity'] += 1
            cart[product_id]['item_total'] = float(product.price * cart[product_id]['quantity'])
        else:
            cart[product_id] = {'quantity':1}
            cart[product_id]['item_total'] = float(product.price * cart[product_id]['quantity'])
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart_view')


def remove_from_cart(request, pk):
    """
     pk = get product id 
     cart, create = if cart exist so get else create
     cart_item = remove cart item if exist while quantity > 1 else remove from cart
    """
    product = get_object_or_404(Product, id=pk)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item = get_object_or_404(CartItem, product=product, cart=cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return redirect("cart_view")
        else:
            cart_item.delete()
            return redirect("cart_view")
    else:
        cart = request.session.get('cart', {})
        # print(request.session.items())
        product_id = str(product.id)

        if product_id in cart:
            if cart[product_id]['quantity'] > 1:
                cart[product_id]['quantity'] -= 1
                cart[product_id]['item_total'] = float(product.price * cart[product_id]['quantity'])
            else:
                del cart[product_id]
        request.session['cart'] =cart
        request.session.modified = True
        return redirect('cart_view')


        
