from django import forms
from .models import Item, Customer


class ItemQuickForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'description', 'retail_price', 'thumbnail', )
        model = Item


class ItemForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'description', 'notes', 'stock', 'cost_price', 'retail_price', 'thumbnail',
                  'image1', 'image2', 'image3', )
        model = Item


class CustomerQuickForm(forms.ModelForm):
    class Meta:
        fields = ('company_name', 'name', 'email')
        model = Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        fields = ('company_name', 'name')
        model = Customer
