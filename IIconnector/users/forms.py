from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import SelectDateWidget, Textarea

from users.models import CustomUser


class LoginForm(forms.Form):
    user_login = forms.CharField(label='Логин', max_length=50)
    user_password = forms.CharField(label='Пароль', max_length=12, widget=forms.PasswordInput())

    user_login.widget.attrs.update({'class': 'form-control', 'placeholder': ' логин'})
    user_password.widget.attrs.update({'class': 'form-control', 'placeholder': 'пароль'})


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'phone', 'email', 'password')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'phone', 'email', 'is_staff')
