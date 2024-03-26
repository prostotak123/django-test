from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username", "class": "input100"})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "input100"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "input100"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Password", "class": "input100"}
        )
    )

    class Meta:
        model = User
        fields = ["username", "email"]
