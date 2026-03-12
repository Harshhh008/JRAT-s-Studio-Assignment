from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .custom_manager import CustomManager
import uuid


class User(AbstractBaseUser, PermissionsMixin):
  """user model with custom fields"""
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  email = models.EmailField(unique=True, max_length=200)
  username = models.CharField(unique=True, max_length=200, blank=True)
  first_name = models.CharField(max_length=200, null=True, blank=True)
  last_name = models.CharField(max_length=200, null=True, blank=True)
  phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
  date_of_birth = models.DateField(null=True, blank=True)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.email)
  
  USERNAME_FIELD = 'email'

  class Meta:
    ordering = ['-created_at']
  
  objects = CustomManager()

  """auto generate if username is blank"""
  def save(self, *args, **kwargs):
    if not self.username:
      self.username = self.email.split("@")[0]
    super().save(*args, **kwargs)
  
  @property
  def full_name(self):
    return f"{self.first_name if self.first_name else ''} {self.last_name if self.last_name else ''}"


class UserAddress(models.Model):
  """user can create multiple address"""
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
  house_num = models.CharField(max_length=50, help_text="enter your building/house number e.g: F/406")
  building_name = models.CharField(max_length=100, help_text="enter your building name")
  area = models.CharField(max_length=100, null=True, blank=True)
  city = models.CharField(max_length=100, null=True, blank=True)
  state = models.CharField(max_length=100, null=True, blank=True)
  pincode = models.CharField(max_length=10, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name_plural = 'User Addresses'

  def __str__(self):
    return f"{self.user.username} -> {self.area}"
  
  @property
  def full_address(self):
    return f"{self.house_num if self.house_num else ''}, {self.building_name if self.building_name else ''}, {self.area if self.area else ''}, {self.city if self.city else ''}, {self.state if self.state else ''}, {self.pincode if self.pincode else ''}."
