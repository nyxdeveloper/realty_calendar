# django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = (
            "phone",
            "email",
            "first_name",
            "last_name",
            "password",
            "subscription",
            "manager",
            "is_active",
            "is_staff",
            "is_superuser",
            "comment",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "phone",
            "email",
            "first_name",
            "last_name",
            "password",
            "subscription",
            "manager",
            "is_active",
            "is_staff",
            "is_superuser",
            "comment",
        )
