from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from accounts.forms import UserLoginForm

# Create your views here.
def dashboardView(request):
    return render(request, 'utils/dashboard.html')


def homepage(request):
    form = UserLoginForm()
    context = {
        'form': form,
    }
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have login in successfully.')
            return redirect('dashboard')
        else:
            form = UserLoginForm(request.POST)
            context['form'] = form
            messages.error(request, 'Account Number or password is incorrect')
            return render(request, 'utils/index.html', context)
    else:
        return render(request, 'utils/index.html', context)