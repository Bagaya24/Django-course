from django import forms
from . import models

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="",
                                         widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full name'}))
    shipping_email = forms.EmailField(label="",
                                      widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    shipping_address1 = forms.CharField(label="",
                                        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}))
    shipping_address2 = forms.CharField(label="",
                                        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}))
    shipping_city = forms.CharField(label="",
                                    widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}))
    shipping_province = forms.CharField(label="",
                                        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Province'}), required=False)
    shipping_zipcode = forms.CharField(label="",
                                       widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), required=False)
    shipping_country = forms.CharField(label="",
                                       widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country '}))

    class Meta:
        model = models.ShippingAddress
        fields = ["shipping_full_name", "shipping_email", "shipping_address1", "shipping_address2","shipping_city",
                  "shipping_province", "shipping_zipcode", "shipping_country"]
        exclude = ["user",]

class PaymentForm(forms.Form):
    card_name = forms.CharField(label="",
                                       widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card name '}))
    card_number = forms.IntegerField(label="",
                                       widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card number '}))
    card_exp_date = forms.DateTimeField(label="",
                                       widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Exp Date '}))
    card_cvv_number = forms.IntegerField(label="",
                                       widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV number '}))
    card_address1 = forms.CharField(label="",
                                       widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Address1 '}))
    card_address2 = forms.CharField(label="",
                                       widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Address2 '}), required=False)
    card_city = forms.CharField(label="",
                                       widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card City '}))
    card_state = forms.CharField(label="",
                                       widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card State '}))
    card_zipcode = forms.CharField(label="",
                                       widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Zipcode '}))
    card_country = forms.CharField(label="",
                                       widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country '}))