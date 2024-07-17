from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import UtilBill, Household


class HouseholdForm(ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Micheal Amponsah'}))
    contact = forms.CharField(label='Contact', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'0242255888'}))
    user = forms.ModelChoiceField(label='', queryset=User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Household
        fields = ['name', 'contact','user']


class DustbinForm(ModelForm):
    billDate = forms.DateField(label='Date on bill', widget=forms.DateInput(attrs={'class':'form-control', 'type':'date'}))
    dustbinBill = forms.DecimalField(label='Dustbin bill', widget=forms.NumberInput(attrs={'class':'form-control'}))
    electricBill = forms.DecimalField(label='electric bill', widget=forms.NumberInput(attrs={'class':'form-control'}))
    waterBill = forms.DecimalField(label='Water bill', widget=forms.NumberInput(attrs={'class':'form-control'}))
    user = forms.ModelChoiceField(label='', queryset=User.objects.all(), widget=forms.HiddenInput())
    
    class Meta:
        model = UtilBill
        fields = ['billDate', 'dustbinBill','electricBill','waterBill']