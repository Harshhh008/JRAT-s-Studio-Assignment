from .models import Category

def category_list(request):
  return {
    'categories' : Category.objects.values('category_name').order_by('category_name')
  }