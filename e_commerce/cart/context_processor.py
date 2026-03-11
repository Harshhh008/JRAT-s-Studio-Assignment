def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        from .models import CartItem
        cart = CartItem.objects.select_related('cart').filter(cart__user=request.user)
        if cart:
            count = cart.count()  
    return {'cart_count': count}