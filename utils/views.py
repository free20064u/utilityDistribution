from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from accounts.forms import UserLoginForm
from .forms import DustbinForm, HouseholdForm, ApplianceForm
from .models import UtilBill, Household, Appliance

# Create your views here.
def editApplianceView(request, id=None):
    form = ApplianceForm(instance=Appliance.objects.get(id=id))
    context = {
        'form': form,
        'edit': True,
    }
    if request.method == 'POST':
        form = ApplianceForm(request.POST, instance=Appliance.objects.get(id=id))
        if form.is_valid():
            form.save()
            messages.success(request, 'Appliance edited successfully')
            return redirect('electricalAppliance')
        else:
            messages.error(request, 'Applaince edit not successful')
            return render(request, 'utils/addAppliance.html', context)
    else:
        return render(request, 'utils/addAppliance.html', context)

def addApplianceView(request):
    form = ApplianceForm()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = ApplianceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New appliance added')
            return redirect('electricalAppliance')
        else:
            messages.error(request, 'Appliance not added')
            return render(request, 'utils/addAppliance.html', context)  
    else: 
        return render(request, 'utils/addAppliance.html', context)
    

def electricalApplianceView(request):
    appliances = Appliance.objects.all().order_by('name')
    context = {
        'appliances': appliances,
    }
    return render(request, 'utils/electricAppliance.html', context)



def editHouseholdView(request, id=None):
    form = HouseholdForm(instance=Household.objects.get(id=id))
    context = {
        'form': form,
        'edit': True,
    }
    if request.method == 'POST':
        form = HouseholdForm(request.POST, instance=Household.objects.get(id=id))
        if form.is_valid():
            form.save()
            messages.success(request, 'Household edit successfully')
            return redirect('household')
        else:
            return render(request, 'utils/addHousehold.html', context)
    else:
        return render(request, 'utils/addHousehold.html', context)


def addHouseholdView(request):
    form = HouseholdForm(initial={'user':request.user})
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = HouseholdForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            messages.success(request, 'Household added')
            return redirect('household')
        else:
            context['form'] = form
            messages.error(request, 'Household not added')
            return render(request, 'utils/addHousehold.html', context)
    else:
        return render(request, 'utils/addHousehold.html', context)


def householdView(request):
    households = Household.objects.all().order_by('name')
    context = {
        'households': households,
    }
    return render(request, 'utils/household.html', context)


def editBillView(request, id=None):
    oldBill = UtilBill.objects.get(id=id)
    form = DustbinForm(instance=oldBill, initial={'dustbinBill':oldBill.dustbinBill, 'electricBill':oldBill.electricBill, 'waterBill':oldBill.waterBill, 'user':request.user})
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = DustbinForm(request.POST, instance=UtilBill.objects.get(id=id))
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