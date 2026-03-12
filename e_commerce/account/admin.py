from django.contrib import admin
from .models import User, UserAddress
from django.contrib.auth.admin import UserAdmin as BaseAdmin


@admin.register(User)
class UserAdmin(BaseAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "full_name",
        "date_of_birth",
        "phone_number",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_display_links = ("email",)
    list_filter = ("is_superuser", "is_active", "is_staff")
    search_fields = ("email", "username", "phone_number")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "Personal Details",
            {
                "fields": ("username","first_name","last_name", "phone_number", "date_of_birth"),
            },
        ),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
        ("Extra Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important Dates", {"fields": ("created_at", "updated_at")}),
    )
    add_fieldsets = (
      ("Create User",
        { 
            "fields": ("email", "username", "password1", "password2") 
        }
      ),
    )


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
  list_display = ['user__email', 'house_num', 'building_name', 'area', 'city', 'state', 'pincode']
  list_filter = ['city', 'state']
  search_fields = ['user', 'area', 'city', 'state', 'pincode']
  fieldsets = (
      ("User", { "fields": ( 'user', ), }),
      ("Address Fields", { "fields": ('house_num', 'building_name', 'area', 'city', 'state', 'pincode')}),
      ("Full Address", {"fields": ('full_address',)}),
      ("Important Dates", {"fields": ('created_at','updated_at')}),
  )
  
  readonly_fields = ['full_address', 'created_at', 'updated_at']
