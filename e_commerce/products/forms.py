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
  
  def __init__(self, *args, **kwargs):
    self.product = kwargs.pop('product', None)
    super().__init__(*args, **kwargs)
  
  def clean_image(self):
    image = self.cleaned_data.get('image')
    if self.product and ProductImage.objects.filter(image=image.name).exists():
      raise forms.ValidationError('Image already exist.')
    return image