from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User

class UserRegisterationForm(ModelForm):
    first_name = forms.CharField(label='First name', widget = forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='Last name', widget = forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(label='Username', widget = forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(label='Email', widget = forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField( label='Password', widget = forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField( label='Password Confirm', widget= forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']


class UserLoginForm(ModelForm):
    username = forms.CharField( label='Username', widget= forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField( label='Password', widget= forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields =['username', 'password']
