from django.db import models
import uuid
from django.core.validators import MinValueValidator
from django.utils.text import slugify

"""auto create nested folder to store separate images based on category"""


def product_image_upload_path(instance, filename):
    # print(instance, filename)
    # print(dir(instance))
    category = slugify(instance.product.category.category_name)
    product = slugify(instance.product.product_name)
    # print(category, product)
    return f"products/{category}/{product}/{filename}"


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    """store category"""

    category_name = models.CharField(unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "categories"


class Product(BaseModel):
    """store product details"""

    product_name = models.CharField(max_length=200)
    product_slug = models.SlugField(max_length=300, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product"
    )
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return str(self.product_name)


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_image"
    )
    image = models.ImageField(
        upload_to=product_image_upload_path, null=True, blank=True
    )

    def __str__(self):
        return str(self.product.product_name)
