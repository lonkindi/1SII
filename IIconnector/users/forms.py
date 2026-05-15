from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import SelectDateWidget, Textarea

from users.models import CustomUser


class LoginForm(AuthenticationForm):
    
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    
    username.widget.attrs.update({'class': 'form-control', 'placeholder': ' логин'})
    password.widget.attrs.update({'class': 'form-control', 'placeholder': 'пароль'})


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'phone', 'email', 'password')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'phone', 'email', 'is_staff')
