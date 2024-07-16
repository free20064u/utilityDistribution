from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from accounts.forms import UserLoginForm
from .forms import DustbinForm
from .models import UtilBill

# Create your views here.
def editBillView(request, id=None):
    oldBill = UtilBill.objects.get(id=id)
    form = DustbinForm(instance=oldBill, initial={'dustbinBill':oldBill.dustbinBill, 'electricBill':oldBill.electricBill, 'waterBill':oldBill.waterBill, 'user':request.user})
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = DustbinForm(request.POST, instance=UtilBill.objects.get(id=id))
        print(form)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user
            bill.save()
            messages.success(request, 'This month bill edited.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Bill not edited.')
            return render(request, 'utils/dustbin.html', context)
    else:
        return render(request, 'utils/dustbin.html', context)


def billsView(request):
    bills = UtilBill.objects.filter(user_id=request.user.id).order_by('-dateAdded')
    context= {
        'bills': bills,
    }
    return render(request, 'utils/bills.html', context)


def utilityBillsView(request):
    form = DustbinForm(initial={'dustbinBill':0.00, 'electricBill':0.00, 'waterBill':0.00, 'user':request.user})
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = DustbinForm(request.POST)
        print(form)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user
            bill.save()
            messages.success(request, 'This month bill added.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Bill not entered.')
            return render(request, 'utils/dustbin.html', context)
    else:
        return render(request, 'utils/dustbin.html', context)
    

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