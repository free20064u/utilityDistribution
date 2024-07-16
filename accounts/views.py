from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib.auth import logout
from django.contrib import messages
from .forms import UserRegisterationForm

# Create your views here.
def registerView(request):
    form = UserRegisterationForm()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.set_password(request.POST['password'])
            client.save()
            messages.success(request, 'Registration successful. Login now')
            return redirect('home')
        else:
            context['form'] = form
            return render(request, 'accounts/register.html', context)
    else:
        return render(request, 'accounts/register.html', context)

def signOutView(request):
    logout(request)
    messages.error(request, 'Logged Out')
    return redirect('home')