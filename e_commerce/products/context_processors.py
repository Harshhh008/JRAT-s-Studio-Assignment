from .models import Category
from django.contrib.auth.decorators import permission_required

def category_list(request):
  return {
    'categories' : Category.objects.values('id','category_name').order_by('category_name')
  }