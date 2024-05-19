# forms.py

from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    phoneNumber = forms.CharField(max_length=10, label='Phone Number', widget=forms.TextInput(attrs={'pattern': '[0-9]{10}'}))
