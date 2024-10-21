from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):

    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}), required=True)
    shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=True)
    shipping_address_1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}), required=True)
    shipping_address_2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}), required=False)
    shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=True)
    shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
    shipping_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), required=False)
    shipping_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=True)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address_1', 'shipping_address_2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country']

        exclude = ['user',]

class PaymentForm(forms.Form):
    card_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name on Card'}), required=True)
    card_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}), required=True)
    card_exp_date = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Expiry date'}), required=True)
    card_cvv_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV'}), required=True)
    card_address_1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address Line 1'}), required=True)
    card_address_2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address Line 2'}), required=False)
    card_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=True)
    card_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=True)
    card_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), required=True)
    card_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=True)