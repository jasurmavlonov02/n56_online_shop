from django import forms
from phonenumber_field.modelfields import PhoneNumberField


class OrderForm(forms.Form):
    full_name = forms.CharField()
    phone_number = PhoneNumberField(region='UZ')
    quantity = forms.IntegerField()


class OrderModelForm(forms.ModelForm):
    pass
