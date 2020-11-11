from django import forms
from django.contrib.auth import forms as user_forms

from .models import CustomUser


class CustomUserCreationForm(user_forms.UserCreationForm):
    class Meta():
        model = CustomUser
        fields = '__all__'


class CustomUserChangeForm(user_forms.UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserLoginForm(user_forms.AuthenticationForm, forms.ModelForm):
    """Форма для авторизации"""

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CustomUserRegistrationForm(user_forms.UserCreationForm):
    """Форма для регистрации"""

    class Meta():
        model = CustomUser
        fields = ('username', 'last_name', 'first_name', 'middle_name', 'is_expert', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
