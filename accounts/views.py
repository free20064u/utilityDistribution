from django.shortcuts import render, redirect
#from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import UserRegisterationForm, UserProfilePicForm, EditUserForm
from utils.models import UserProfilePic


# Create your views here.
def editUserDetailView(request, id=None):
    instance = User.objects.get(id=id)
    form = EditUserForm(instance=instance)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your information has been editted successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Details not editted')
            return render(request, 'accounts/editUserDetail.html', context)
    else:
        return render(request, 'accounts/editUserDetail.html', context)
    


def editUserPicView(request, id=None):
    instance = UserProfilePic.objects.get(user_id=id)
    form = UserProfilePicForm(instance=instance)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = UserProfilePicForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile picture updated')
            return redirect('household')
        else:
            context['form'] = form
            messages.error(request, 'Profile picture not updated')
            return render(request, 'accounts/editUser.html', context)
    else:
        return render(request, 'accounts/editUser.html', context)


def registerView(request):
    form = UserRegisterationForm()
    #form2 = UserProfileForm()
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