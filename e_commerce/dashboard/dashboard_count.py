from products.models import Product, Category
from account.models import User
from order.models import OrderItem

def dashboard_counts(request):
    if 'dashboard' in request.path:
        return {
            'products_count': Product.objects.count(),
            'categories_count': Category.objects.count(),
            'users_count': User.objects.count(),
            'order_items_count': OrderItem.objects.count(),
        }
    return {}