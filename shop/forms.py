from django import forms
from phonenumber_field.modelfields import PhoneNumberField

from shop.models import Product, Comment


class OrderForm(forms.Form):
    full_name = forms.CharField()
    phone_number = PhoneNumberField(region='UZ')
    quantity = forms.IntegerField()


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        # exclude = ()


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name','email','content']
