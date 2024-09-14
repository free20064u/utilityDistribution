from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import MonthlyBill, Household, Appliance, Payment, NumberOfIndividuals, HouseholdAppliance, UserProfilePic, Enquiry



class EnquiryForm(ModelForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control mb-2','placeholder':'example@gmail.com'}))
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'class':'form-control mb-2','placeholder':'enter bills'}))
    message = forms.CharField(label='Name', widget=forms.Textarea(attrs={'class':'form-control mb-2','placeholder':'messages'}))
    
    class Meta:
        model = Enquiry
        fields =['email', 'title', 'message']


class SearchForm(forms.Form):
    choices = [(bill.dateOnBill.strftime('%d-%m-%Y'), bill.dateOnBill.strftime('%d-%m-%Y')) for bill  in MonthlyBill.objects.all().order_by('-dateOnBill')]
    
    dateOnBill = forms.ChoiceField(label='', widget=forms.Select(attrs={'class':'form-control px-5'}), choices=choices)


class UserProfileForm(ModelForm):
    image = forms.ImageField()

    class Meta:
        model = UserProfilePic
        fields = ['image', 'user']


class PaymentForm(ModelForm):
    amount = forms.DecimalField(label='Amount', widget=forms.NumberInput(attrs={'class': 'form-control mb-2'}))
    household = forms.ModelChoiceField(label='', queryset=Household.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = Payment
        fields = ['amount', 'household']


class ApplianceForm(ModelForm):
    name = forms.CharField(label='Appliance Name', widget=forms.TextInput(attrs={'class':'form-control mb-2','placeholder':'Fridge'}))
    power = forms.CharField(label='Power(W)', widget=forms.TextInput(attrs={'class':'form-control mb-2','placeholder':'200'}))
    user = forms.ModelChoiceField(label='', queryset=User.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = Appliance
        fields = ['name', 'power', 'user']



class HouseholdForm(ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class':'form-control mb-2','placeholder':'Micheal Amponsah'}))
    contact = forms.CharField(label='Contact', widget=forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'0242255888'}))
    user = forms.ModelChoiceField(label='', queryset=User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Household
        fields = ['name', 'contact','user', 'image']


class MonthlyBillForm(ModelForm):
    dateOnBill = forms.DateField(label='Date on bill', widget=forms.DateInput(attrs={'class':'form-control mb-2', 'type':'date'}))
    refuseBill = forms.DecimalField(label='Dustbin bill', widget=forms.NumberInput(attrs={'class':'form-control mb-2'}))
    electricityBill = forms.DecimalField(label='electric bill', widget=forms.NumberInput(attrs={'class':'form-control mb-2'}))
    waterBill = forms.DecimalField(label='Water bill', widget=forms.NumberInput(attrs={'class':'form-control mb-2'}))
    user = forms.ModelChoiceField(label='', queryset=User.objects.all(), widget=forms.HiddenInput())
    
    class Meta:
        model = MonthlyBill
        fields = ['dateOnBill', 'refuseBill','electricityBill','waterBill']

    
class NumberOfIndividualsForm(ModelForm):
    dateOnBill = forms.CharField(label='Date On Bill', widget=forms.DateInput(attrs={'class': 'form-control mb-2', 'type':'date'}))
    numberOfIndividuals = forms.DecimalField(label='Number Of Individuals', widget=forms.NumberInput(attrs={'class': 'form-control mb-2'}))
    household = forms.ModelChoiceField(label='', queryset=Household.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = NumberOfIndividuals
        fields = ['dateOnBill', 'numberOfIndividuals', 'household']



class HouseholdApplianceForm(ModelForm):
    #dateOnBill = forms.CharField(label='Date On Bill', widget=forms.HiddenInput(attrs={'class':'form-control mb-2', 'type':'date'}))
    household = forms.ModelChoiceField(label='', queryset=Household.objects.all(), widget=forms.HiddenInput())
    appliance = forms.ModelChoiceField(label='Appliance Name',queryset=Appliance.objects.all(), widget=forms.Select(attrs={'class':'form-control mb-2','placeholder':'Fridge'}))
    quantity = forms.CharField(label='Quantity', widget=forms.NumberInput(attrs={'class':'form-control mb-2'}))
    class Meta:
        model = HouseholdAppliance
        fields = [ 'appliance', 'quantity', 'household']