from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.forms import formset_factory
from django.http import HttpResponse
from git import Repo
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
from decimal import Decimal



from accounts.forms import UserLoginForm
from .forms import (MonthlyBillForm, HouseholdForm, ApplianceForm, PaymentForm, 
                    NumberOfIndividualsForm, HouseholdApplianceForm, SearchForm)

from .models import (MonthlyBill, Household, Appliance, NumberOfIndividuals, 
                     Payment, HouseholdAppliance, Debt)

from .signals import checkHouseholdparameters

now = datetime.now()


# # Create your views here.
@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        repo = Repo('./django-schools')
        git = repo.git
        git.checkout('master')
        git.pull()
        return HttpResponse('pulled_success')
    return HttpResponse('get_request', status=400)


def editNoOfPeopleView(request, id=None):
    noOfPeople = NumberOfIndividuals.objects.get(entryDate__month=now.month, entryDate__year=now.year, household=Household.objects.get(id=id))
    
    if request.method == 'POST':
        form = NumberOfIndividualsForm(request.POST, instance=noOfPeople)
        if form.is_valid():
            form.save()
            return redirect('household')
    else:
        form = NumberOfIndividualsForm(instance=noOfPeople)
        context = {
            'form': form,
        }
        return render(request, 'utils/addPeople.html',context)
    

def addPeopleView(request, id=None):
    household = Household.objects.get(id=id)
    form = NumberOfIndividualsForm(initial={'household':Household.objects.get(id=id)})
    context = {
        'form': form,
        'household': household,
    }
    
    if request.method == 'POST':

        billDate = request.POST['dateOnBill']
        dateformate ='%Y-%m-%d'
        dateOnBill = datetime.strptime(billDate,dateformate)
   
        form = NumberOfIndividualsForm(request.POST)
        if form.is_valid():
            object, created = NumberOfIndividuals.objects.update_or_create(dateOnBill__month=dateOnBill.month, dateOnBill__year=dateOnBill.year, household_id=id, defaults={'numberOfIndividuals':request.POST['numberOfIndividuals'], 'dateOnBill':dateOnBill})
            if created:
                message = 'created'
            else:
                message = 'updated'
            messages.success(request, f'Number of people for this household for this month has been {message}')
            print(created, object)
            return redirect('household')
        else:
            messages.error(request, 'Number of people for this month not saved')
            return render(request, 'utils/addPeople.html', context)
    else:
        return render(request, 'utils/addPeople.html', context)


def payBillView(request, id=None):

    form = PaymentForm(initial={'household':Household.objects.get(id=id)})
    payments = Payment.objects.filter(household_id=id)
    household = Household.objects.get(id=id)
    context = {
        'form': form,
        'payments': payments,
        'household': household,
        
    }
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            pay = form.save(commit=False)
            pay.household = Household.objects.get(id=id)
            pay.save()
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
    appliances = Appliance.objects.filter(user=request.user.id).order_by('name')
    # Initials to be used in the formset
    initial=[{'appliance': appliance,'household':Household.objects.get(id=id), 'dateOnBill':MonthlyBill.objects.last().dateOnBill} for appliance in appliances]
    # Formset for the appliance used by the households
    applianceformset = formset_factory(HouseholdApplianceForm, max_num=appliances.count())
    formset = applianceformset(initial=initial)

    household = Household.objects.get(id=id)

    context = {
        'formset': formset,
        'household': household,
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
    household = Household.objects.get(id=id)
    payments = Payment.objects.filter(household_id=id)
    currentNumberOfPeople=None
    householdAppliance=[]
    householdTotalBill=Decimal(0)
    householdWaterBill=Decimal(0)
    householdElectricityBill=Decimal(0)
    householdRefuseBill=Decimal(0)
    amountDue=Decimal(0)
    form = SearchForm()
    
    if request.method == 'POST':
        billDate = request.POST['dateOnBill']
        dateformate ='%d-%m-%Y'
        now = datetime.strptime(billDate,dateformate)
    else:
        now = datetime.now()


    if (checkHouseholdparameters(dateOnBill=now,household_id=id, user_id=request.user.id)):


        if request.method == "POST":
            billDate = request.POST['dateOnBill']
            dateformate ='%d-%m-%Y'
            billDate = datetime.strptime(billDate,dateformate)
            print(billDate.month)
            print(billDate.year)
            # Household appliance for the current month
            householdAppliance = HouseholdAppliance.objects.filter(dateOnBill__month=billDate.month, dateOnBill__year=billDate.year, household_id=id)

            # Total power consumed by household
            householdPowerConsumed = 0
            for appliance in householdAppliance:
                householdPowerConsumed += appliance.totalPower()


            # All appliances by all the household
            householdsappliances = HouseholdAppliance.objects.filter(dateOnBill__month=billDate.month, dateOnBill__year=billDate.year)

            # Total power consumed by all the appliances in all the household
            householdAppliancesPowerConsumed = 0
            for householdAppliances in householdsappliances:
                householdAppliancesPowerConsumed += householdAppliances.totalPower()

            # Select the current month number of people for household
            currentNumberOfPeople = NumberOfIndividuals.objects.get(dateOnBill__month=billDate.month, household_id=id)

            # Get the total number of people in all the household for the current month
            totalNumberOfPeople = NumberOfIndividuals.totalNumberOfPeopel(NumberOfIndividuals,month=billDate.month, year=billDate.year)
            
            # Get current bill of the month
            currentmonthlyBills = MonthlyBill.objects.get(dateOnBill__month=billDate.month, dateOnBill__year=billDate.year, user_id=request.user.id)

            # Current household water bill.
            if currentmonthlyBills.waterBill != Decimal(0):
                householdWaterBill = currentNumberOfPeople.numberOfIndividuals*currentmonthlyBills.waterBill/totalNumberOfPeople
            # Current household refuse bill
            if currentmonthlyBills.refuseBill != Decimal(0.00):
                householdRefuseBill = currentmonthlyBills.refuseBill/Household.objects.filter(user_id=request.user.id).count()

            # Current household electricity bill
            if currentmonthlyBills.electricityBill != Decimal(0.00):
                householdElectricityBill = householdPowerConsumed * currentmonthlyBills.electricityBill / householdAppliancesPowerConsumed
    
            
            # Household total bill for the month
            householdTotalBill = householdWaterBill + householdRefuseBill + householdElectricityBill

            totalDebt = Debt.householdTotalDebt(Debt, household_id=id)
            totalPayment = Payment.householdTotalPayment(Payment, household_id=id )
            amountDue = totalDebt - totalPayment
            context = {
                'household': household,
                'payments': payments,
                'currentMonthNumberOfPeople': currentNumberOfPeople,
                'householdAppliance': householdAppliance,
                'householdTotalBill': ("{:0.2f}".format(householdTotalBill)),
                'householdWaterBill': ("{:0.2f}".format(householdWaterBill)),
                'householdRefuseBill': ("{:0.2f}".format(householdRefuseBill)),
                'householdElectricityBill': ("{:0.2f}".format(householdElectricityBill)),
                'amountDue': ("{:0.2f}".format(amountDue)),
                'form': form,
            }

            return render(request, 'utils/profile.html', context)

        else: 

            
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
            if currentmonthlyBills.waterBill != Decimal(0):
                householdWaterBill = currentNumberOfPeople.numberOfIndividuals*currentmonthlyBills.waterBill/totalNumberOfPeople
            # Current household refuse bill
            if currentmonthlyBills.refuseBill != Decimal(0.00):
                householdRefuseBill = currentmonthlyBills.refuseBill/Household.objects.all().count()

            # Current household electricity bill
            if currentmonthlyBills.electricityBill != Decimal(0.00):
                householdElectricityBill = householdPowerConsumed * currentmonthlyBills.electricityBill / householdAppliancesPowerConsumed
            
            # Household total bill for the month
            householdTotalBill = householdWaterBill + householdRefuseBill + householdElectricityBill

            totalDebt = Debt.householdTotalDebt(Debt, household_id=id)
            totalPayment = Payment.householdTotalPayment(Payment, household_id=id )
            amountDue = totalDebt - totalPayment

            context = {
                'household': household,
                'payments': payments,
                'currentMonthNumberOfPeople': currentNumberOfPeople,
                'householdAppliance': householdAppliance,
                'householdTotalBill': ("{:0.2f}".format(householdTotalBill)),
                'householdWaterBill': ("{:0.2f}".format(householdWaterBill)),
                'householdRefuseBill': ("{:0.2f}".format(householdRefuseBill)),
                'householdElectricityBill': ("{:0.2f}".format(householdElectricityBill)),
                'amountDue': ("{:0.2f}".format(amountDue)),
                'form': form,
            }
            return render(request, 'utils/profile.html', context)
    else:
        context = {
            'household': household,
            'payments': payments,
            'currentMonthNumberOfPeople': currentNumberOfPeople,
            'householdAppliance': householdAppliance,
            'householdTotalBill': ("{:0.2f}".format(householdTotalBill)),
            'householdWaterBill': ("{:0.2f}".format(householdWaterBill)),
            'householdRefuseBill': ("{:0.2f}".format(householdRefuseBill)),
            'householdElectricityBill': ("{:0.2f}".format(householdElectricityBill)),
            'amountDue': ("{:0.2f}".format(amountDue)),
            'form': form,
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
    appliances = Appliance.objects.filter(user=request.user.id).order_by('name')
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
        form = HouseholdForm(request.POST, request.FILES, instance=Household.objects.get(id=id))
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
        form = HouseholdForm(request.POST, request.FILES)
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
    households = Household.objects.filter(user=request.user.id).order_by('name')
    context = {
        'households': households,
    }
    return render(request, 'utils/household.html', context)


def editBillView(request, id=None):
    oldBill = MonthlyBill.objects.get(id=id)
    form = MonthlyBillForm(instance=oldBill, initial={'dustbinBill':oldBill.refuseBill, 
                                                      'electricBill':oldBill.electricityBill, 'waterBill':oldBill.waterBill, 
                                                      'user':request.user})
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
    form = MonthlyBillForm(initial={'refuseBill':0.00, 
                                    'electricityBill':0.00, 
                                    'waterBill':0.00, 
                                    'user':request.user})
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
    monthlyBill = MonthlyBill.objects.filter(user_id=request.user.id)
    totalWaterBill=0
    totalRefuseBill=0
    totalElectricityBill=0
    waterBillList = ''
    refuseBillList = ''
    electricityBillList = ''
    dateOnBillList = ''
    #Creating list of waterbill, electricity bill and refuse bill to be used by javascript to create array for drawing of graph
    for bill in monthlyBill:
        totalWaterBill += bill.waterBill
        totalRefuseBill += bill.refuseBill
        totalElectricityBill += bill.electricityBill
        waterBillList += f'{int(bill.waterBill)} '
        refuseBillList += f'{int(bill.refuseBill)} '
        electricityBillList += f'{int(bill.electricityBill)} '
        dateOnBillList += f'{(datetime.strftime(bill.dateOnBill, "%d-%m-%Y"))} ' 

    context = {
        'totalWaterBill': totalWaterBill,
        'totalRefuseBill': totalRefuseBill,
        'totalElectricityBill': totalElectricityBill,
        'waterBillList': waterBillList,
        'refuseBillList': refuseBillList,
        'electricityBillList': electricityBillList,
        'dateOnBillList': dateOnBillList,
    }
    return render(request, 'utils/dashboard.html',context)


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