from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from decimal import Decimal

from .models import Household, NumberOfIndividuals, MonthlyBill, HouseholdAppliance, Debt, UserProfile


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwarg):
    if created:
        UserProfile.objects.create(user=instance)



def checkparameters(dateOnBill=None, user_id=None):
    households = Household.objects.filter(user_id=user_id)
    for household in households:

        # Household appliance for the current month
        householdAppliance = HouseholdAppliance.objects.filter(dateOnBill__month=dateOnBill.month, dateOnBill__year=dateOnBill.year, household_id=household.id)
        if householdAppliance.count() < 1:
            return False

        # Select the current month number of people for household
        try:
            currentNumberOfPeople = NumberOfIndividuals.objects.get(dateOnBill__month=dateOnBill.month, household_id=household.id)

            # Get current bill of the month
            currentmonthlyBills = MonthlyBill.objects.get(dateOnBill__month=dateOnBill.month, dateOnBill__year=dateOnBill.year, user_id=user_id)
        except:
            return False
        
    return True

def checkHouseholdparameters(dateOnBill=None,household_id=None, user_id=None):
    household = Household.objects.get(id=household_id)

    # Household appliance for the current month
    householdAppliance = HouseholdAppliance.objects.filter(dateOnBill__month=dateOnBill.month,dateOnBill__year=dateOnBill.year, household_id=household.id)
    if householdAppliance.count() < 1:
        return False

        # Select the current month number of people for household
    try:
        currentNumberOfPeople = NumberOfIndividuals.objects.get(dateOnBill__month=dateOnBill.month, household_id=household.id)

            # Get current bill of the month
        currentmonthlyBills = MonthlyBill.objects.get(dateOnBill__month=dateOnBill.month, dateOnBill__year=dateOnBill.year, user_id=user_id)
    except:
        return False
    
    return True
        


def updateBill(dateOnBill=None, household_id=None, user_id=None):

    householdTotalBill=Decimal(0)
    householdWaterBill=Decimal(0)
    householdElectricityBill=Decimal(0)
    householdRefuseBill=Decimal(0)
   
    
    # Household appliance for the current month
    householdAppliance = HouseholdAppliance.objects.filter(dateOnBill__month=dateOnBill.month, dateOnBill__year=dateOnBill.year, household_id=household_id)
   
    # Total power consumed by household
    householdPowerConsumed = 0
    for appliance in householdAppliance:
        householdPowerConsumed += appliance.totalPower()


    # All appliances by all the household 
    householdsappliances = HouseholdAppliance.objects.filter(dateOnBill__month=dateOnBill.month, dateOnBill__year=dateOnBill.year)

    # Select the current month number of people for household
    currentNumberOfPeople = NumberOfIndividuals.objects.get(dateOnBill__month=dateOnBill.month, household_id=household_id)

    # Get the total number of people in all the household for the current month
    totalNumberOfPeople = NumberOfIndividuals.totalNumberOfPeopel(NumberOfIndividuals,month=dateOnBill.month, year=dateOnBill.year)
    
    # Get current bill of the month
    currentmonthlyBills = MonthlyBill.objects.get(dateOnBill__month=dateOnBill.month, dateOnBill__year=dateOnBill.year, user_id=user_id)

    # Total power consumed by all the appliances in all the household
    householdAppliancesPowerConsumed = 0
    for householdAppliances in householdsappliances:
        householdAppliancesPowerConsumed += householdAppliances.totalPower()


    # Current household water bill.
    if currentmonthlyBills.waterBill != Decimal(0):
        householdWaterBill = currentNumberOfPeople.numberOfIndividuals*currentmonthlyBills.waterBill/totalNumberOfPeople
    # Current household refuse bill
    if currentmonthlyBills.refuseBill != Decimal(0.00):
        householdRefuseBill = currentmonthlyBills.refuseBill/Household.objects.filter(user_id=user_id).count()

    # Current household electricity bill
    if currentmonthlyBills.electricityBill != Decimal(0.00):
        householdElectricityBill = householdPowerConsumed * currentmonthlyBills.electricityBill / householdAppliancesPowerConsumed
    
    # Household total bill for the month
    householdTotalBill = householdWaterBill + householdRefuseBill + householdElectricityBill

    print(householdTotalBill, householdWaterBill , householdRefuseBill , householdElectricityBill)

    object, created = Debt.objects.get_or_create(dateOnBill__month=dateOnBill.month, dateOnBill__year=dateOnBill.year, household=Household.objects.get(id=household_id), defaults={'dateOnBill':dateOnBill, 'household_id':household_id, 'totalDept':householdTotalBill})

    if not created:
        object.totalDept=householdTotalBill
        object.save()


@receiver(post_save, sender=NumberOfIndividuals)
def my_handler(sender, instance, **kwargs):
    print(1)

    if (checkparameters(dateOnBill=instance.dateOnBill,user_id=instance.household.user.id)):
        print(2)
        for household in Household.objects.filter(user_id=instance.household.user_id):
            updateBill(dateOnBill=instance.dateOnBill, household_id=household.id, user_id=instance.household.user.id)
        print(3)

@receiver(post_save, sender=MonthlyBill)
def my_handler(sender, instance, **kwargs):
    print(instance.dateOnBill, instance.user.id)

    if (checkparameters(dateOnBill=instance.dateOnBill,user_id=instance.user.id)):
        for household in Household.objects.filter(user_id=instance.household.user_id):
            updateBill(dateOnBill=instance.dateOnBill, household_id=household.id, user_id=instance.user.id)


@receiver(post_save, sender=HouseholdAppliance)
def my_handler(sender, instance, **kwargs):
    print(instance.dateOnBill, instance.household.user.id)

    if (checkparameters(dateOnBill=instance.dateOnBill,user_id=instance.household.user.id)):
        for household in Household.objects.filter(user_id=instance.user_id):
            updateBill(dateOnBill=instance.dateOnBill, household_id=household.id, user_id=instance.household.user.id)
