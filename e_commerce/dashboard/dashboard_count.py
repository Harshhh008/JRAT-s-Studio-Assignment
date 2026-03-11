from products.models import Product, Category
from account.models import User
from order.models import OrderItem

def dashboard_counts(request):
    if 'dashboard' in request.path and (request.user.is_superuser or request.user.is_staff):
        return {
            'products_count': Product.objects.count(),
            'categories_count': Category.objects.count(),
            'users_count': User.objects.count(),
            'order_items_count': OrderItem.objects.count(),
        }
    return {}