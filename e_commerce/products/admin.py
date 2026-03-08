from django.contrib import admin
from .models import Product, ProductImage, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'category_name')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
  list_display = ('id', 'product__product_name', 'image')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = (
    'id',
    'product_name',
    'product_slug',
    'category',
    'description',
    'stock',
    'price',
    'created_at',
    'updated_at'
  )
  readonly_fields = ('created_at', 'updated_at')
  list_filter  = ('category', )
  search_fields = ('category', 'product_name', 'description', 'product_slug')
  prepopulated_fields = {
    "product_slug": ('product_name',)
  }
  ordering = ['-updated_at']
  