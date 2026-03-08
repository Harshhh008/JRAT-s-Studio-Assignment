from django import forms
from .models import Product, Category, ProductImage

class CategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = ['category_name']
  
class ProductForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = "__all__" 
    exclude = ['product_slug']
  
class ProductImageForm(forms.ModelForm):
  class Meta:
    model = ProductImage
    fields = ['image']