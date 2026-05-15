from django.contrib import admin

from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from users.forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):    
    add_fieldsets = ( ( None, { "classes": ("wide",), "fields": ("phone", "password1", "password2"), }, ), )
    list_display = ('phone', 'is_staff', 'is_superuser')
