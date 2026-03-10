from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth import get_user_model
from .models import UserAddress

User = get_user_model()


class UserCreationForm(BaseUserCreationForm):
    """override UserCreationForm with email authentication instant of username"""

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class AuthenticationForm(forms.Form):
    """login form with email and password fields"""
    email = forms.EmailField(max_length=200)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("email"):
            raise forms.ValidationError("Email is required.")
        if not cleaned_data.get("password"):
            raise forms.ValidationError("Password is required.")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = [
            'house_num', 'building_name', 'area', 'city', 'state', 'pincode'
        ]