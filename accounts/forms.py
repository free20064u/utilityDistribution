from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from utils.models import UserProfilePic


class UserProfilePicForm(ModelForm):
    image = forms.ImageField()

    class Meta:
        model = UserProfilePic
        fields = ['image']


class UserRegisterationForm(ModelForm):
    first_name = forms.CharField(label='First name', widget = forms.TextInput(attrs={'class':'form-control mb-2'}))
    last_name = forms.CharField(label='Last name', widget = forms.TextInput(attrs={'class':'form-control mb-2'}))
    username = forms.CharField(label='Username', widget = forms.TextInput(attrs={'class':'form-control mb-2'}))
    email = forms.CharField(label='Email', widget = forms.EmailInput(attrs={'class':'form-control mb-2'}))
    password = forms.CharField( label='Password', widget = forms.PasswordInput(attrs={'class': 'form-control mb-2'}))
    password_confirm = forms.CharField( label='Password Confirm', widget= forms.PasswordInput(attrs={'class': 'form-control mb-2'}))
    #image = forms.ImageField()


    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']


class EditUserForm(ModelForm):
    first_name = forms.CharField(label='First name', widget = forms.TextInput(attrs={'class':'form-control mb-2'}))
    last_name = forms.CharField(label='Last name', widget = forms.TextInput(attrs={'class':'form-control mb-2'}))
    username = forms.CharField(label='Username', widget = forms.TextInput(attrs={'class':'form-control mb-2'}))
    email = forms.CharField(label='Email', widget = forms.EmailInput(attrs={'class':'form-control mb-2'}))


    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']


class UserLoginForm(ModelForm):
    username = forms.CharField( label='Username', widget= forms.TextInput(attrs={'class': 'form-control mb-2'}))
    password = forms.CharField( label='Password', widget= forms.PasswordInput(attrs={'class': 'form-control mb-2'}))

    class Meta:
        model = User
        fields =['username', 'password']
