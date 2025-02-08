from django import forms

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
