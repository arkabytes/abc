from django import forms
from .models import Item, Customer, VatType, DeliveryType, PaymentType, Provider


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
        fields = ('cif', 'company_name', 'name', 'surname', 'address', 'city', 'province',
                  'postal_code', 'country', 'phone', 'fax', 'email', 'web', 'notes')
        model = Customer


class ProviderQuickForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'contact_name', 'email')
        model = Provider


class ProviderForm(forms.ModelForm):
    class Meta:
        fields = ('cif', 'name', 'contact_name', 'address', 'city', 'province',
                  'postal_code', 'country', 'phone', 'fax', 'email', 'web', 'notes')
        model = Provider


class DeliveryTypeForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'description', 'days', 'cost')
        model = DeliveryType


class PaymentTypeForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'description', 'cost')
        model = PaymentType


class VatTypeForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'rate')
        model = VatType
