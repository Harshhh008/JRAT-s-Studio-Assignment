from .models import Category

def category_list(request):
  return {
    'categories' : Category.objects.values('id','category_name').order_by('category_name')
  }