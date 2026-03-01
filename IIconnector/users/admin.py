from django.contrib import admin

from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from users.forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    # fieldsets = (
    #     (_("Personal info"), {"fields": ("first_name", "last_name", "phone", "email", "user_type")}),
    # )
    list_display = ('username', 'phone', 'email', 'is_staff', 'is_superuser')
    # inlines = [InlinehzUserInfo, InlinehzUserEvents, ]


admin.site.register(CustomUser, CustomUserAdmin)