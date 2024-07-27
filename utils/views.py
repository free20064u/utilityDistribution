from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.forms import formset_factory, modelformset_factory

from datetime import datetime

from accounts.forms import UserLoginForm
from .forms import MonthlyBillForm, HouseholdForm, ApplianceForm, PaymentForm, NumberOfIndividualsForm, HouseholdApplianceForm
from .models import MonthlyBill, Household, Appliance, NumberOfIndividuals, Payment,HouseholdAppliance

now = datetime.now()
month = now.month
year = now.year

# # Create your views here.
def addPeopleView(request, id=None):
    household = Household.objects.get(id=id)
    form = NumberOfIndividualsForm(initial={'household':Household.objects.get(id=id)})
    context = {
        'form': form,
        'household': household,
    }
    if request.method == 'POST':
        form = NumberOfIndividualsForm(request.POST)


        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Number of people for this household for this month is added')
            return redirect('household')
        else:
            messages.error(request, 'Number of people for this month not saved')
            return render(request, 'utils/addPeople.html', context)
    else:
        return render(request, 'utils/addPeople.html', context)


def payBillView(request, id=None):
    form = PaymentForm(initial={'user':Household.objects.get(id=id)})
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bill Paid')
            return redirect('household')
        else:
            context['form'] = form
            messages.error(request, 'Household not added')
            return render(request, 'utils/payBill.html', context)
    else:
        return render(request, 'utils/payBill.html', context)


def addHouseholdApplianceView(request, id=None):
    # Get all the appliance to use to populate the initials for the formset
    appliances = Appliance.objects.all().order_by('name')
    # Initials to be used in the formset
    initial=[{'appliance': appliance,'household':Household.objects.get(id=id), 'dateOnBill':MonthlyBill.objects.last().dateOnBill} for appliance in appliances]
    # Formset for the appliance used by the households
    applianceformset = formset_factory(HouseholdApplianceForm, max_num=appliances.count())
    formset = applianceformset(initial=initial)


    context = {
        'formset': formset,
    }

    if request.method == 'POST':
        formset = applianceformset(request.POST, initial=initial)
        if formset.is_valid():
            for form in formset:
                appli = form.save(commit=False)
                appli.dateOnBill = MonthlyBill.objects.last().dateOnBill
                appli.save()
            messages.success(request, 'Appliance for this month added')
            return redirect('household')
        else:
            messages.error(request, 'Appliances not added. Check and add again.')
            context['formset'] = formset
            return render(request, 'utils/addHouseholdAppliance.html', context)
    else:
        return render(request, 'utils/addHouseholdAppliance.html', context)
    

def profileView(request, id=None):
    if request.method == 'POST':
        pass

    household = Household.objects.get(id=id)
    households = Household.objects.all()
    payments = Payment.objects.filter(household_id=id)
    monthlyBills = MonthlyBill.objects.all().order_by('-dateOnBill')
    
    # Household appliance for the current month
    householdAppliance = HouseholdAppliance.objects.filter(dateOnBill__month=now.month, dateOnBill__year=now.year, household_id=id)

    # Total power consumed by household
    householdPowerConsumed = 0
    for appliance in householdAppliance:
        householdPowerConsumed += appliance.totalPower()


    # All appliances by all the household
    householdsappliances = HouseholdAppliance.objects.filter(dateOnBill__month=now.month, dateOnBill__year=now.year)

    # Total power consumed by all the appliances in all the household
    householdAppliancesPowerConsumed = 0
    for householdAppliances in householdsappliances:
        householdAppliancesPowerConsumed += householdAppliances.totalPower()

    # Select the current month number of people for household
    currentNumberOfPeople = NumberOfIndividuals.objects.get(dateOnBill__month=now.month, household_id=id)

    # Get the total number of people in all the household for the current month
    totalNumberOfPeople = NumberOfIndividuals.totalNumberOfPeopel(NumberOfIndividuals,month=now.month, year=now.year)
    
    # Get current bill of the month
    currentmonthlyBills = MonthlyBill.objects.get(dateOnBill__month=now.month, dateOnBill__year=now.year, user_id=request.user.id)

    # Current household water bill.
    householdWaterBill = currentNumberOfPeople.numberOfIndividuals*currentmonthlyBills.waterBill/totalNumberOfPeople
    # Current household refuse bill
    householdRefuseBill = currentmonthlyBills.refuseBill/households.count()
    # Current household electricity bill
    householdElectricityBill = householdPowerConsumed * currentmonthlyBills.electricityBill / householdAppliancesPowerConsumed
    
    # Household total bill for the month
    householdTotalBill = householdWaterBill + householdRefuseBill + householdElectricityBill

    context = {
        'household': household,
        'payments': payments,
        'currentMonthNumberOfPeople': currentNumberOfPeople,
        'householdAppliance': householdAppliance,
        'householdTotalBill': ("{:0.2f}".format(householdTotalBill)),
        'monthlyBills':monthlyBills,
        'householdWaterBill': householdWaterBill,
        'householdRefuseBill': householdRefuseBill,
        'householdElectricityBill': ("{:0.2f}".format(householdElectricityBill)),
    }
    return render(request, 'utils/profile.html', context)


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
    form = ApplianceForm(initial={'user':request.user})
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
    oldBill = MonthlyBill.objects.get(id=id)
    form = MonthlyBillForm(instance=oldBill, initial={'dustbinBill':oldBill.dustbinBill, 'electricBill':oldBill.electricBill, 'waterBill':oldBill.waterBill, 'user':request.user})
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = MonthlyBillForm(request.POST, instance=MonthlyBill.objects.get(id=id))
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
    bills = MonthlyBill.objects.filter(user_id=request.user.id).order_by('-dateOnBill')
    context= {
        'bills': bills,
    }
    return render(request, 'utils/bills.html', context)


def utilityBillsView(request):
    form = MonthlyBillForm(initial={'refuseBill':0.00, 'electricityBill':0.00, 'waterBill':0.00, 'user':request.user})
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = MonthlyBillForm(request.POST)
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