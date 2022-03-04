# from django.contrib import admin
#
# from .models import User
# from .models import Email
#
#
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'id', 'last_name', 'phone', 'is_active', 'subscription', 'comment')
#     list_filter = ['is_active']
#     search_fields = ['first_name', 'last_name', 'phone', 'comment', 'email']
#
#
# admin.site.register(Email)

# django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("id", "phone", "email", "first_name", "last_name", "subscription", "manager", "is_active",
                    "is_staff", "is_superuser", "comment",)
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'manager',)
    fieldsets = (
        ('Основная информация', {'fields': (("phone", "email", "first_name", "last_name"), 'password',)}),
        ('Права', {'fields': ('is_staff', 'is_active', 'is_superuser', 'activist')}),
        ('Подписка', {'fields': ('subscription', 'comment')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                ('phone', 'email'),
                ('password1', 'password2'),
                ("first_name", "last_name",),
                ('is_staff', 'is_active', 'is_superuser', 'manager'),
                "subscription",
            )}
         ),
    )
    search_fields = ("phone", "email", "first_name", "last_name",)
    ordering = ("id", "phone", "email", "first_name", "last_name", "subscription", "manager", "is_active",
                "is_staff", "is_superuser", "comment",)


admin.site.register(User, CustomUserAdmin)
