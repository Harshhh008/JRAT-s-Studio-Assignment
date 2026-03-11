from products.models import Product, Category
from account.models import User

def dashboard_counts(request):
    if 'dashboard' in request.path:
        return {
            'products_count': Product.objects.count(),
            'categories_count': Category.objects.count(),
            'users_count': User.objects.count(),
        }
    return {}