from django import forms
from django.contrib.auth.forms import UserCreationForm

from user.models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email Cannot be None')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('User not Found')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError('Password Cannot be None')
        return password

    # def clean(self):
    #     pass


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150, required=False)
    confirm_password = forms.CharField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is None:
            raise forms.ValidationError('Email can not be None')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This {email} is already registered')
        return email

    # def clean_password(self):
    #     password = self.data.get('password')
    #     confirm_password = self.data.get('confirm_password')
    #     if password != confirm_password:
    #         raise forms.ValidationError('Passwords do not match')
    #     return self.cleaned_data['password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('do not match')
        return cleaned_data
