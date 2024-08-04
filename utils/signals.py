from django.db.models.signals import post_save
from django.dispatch import receiver



from .models import Household, Payment, NumberOfIndividuals, MonthlyBill, HouseholdAppliance, Debt

def checkparameters(dateOnBill=None, user_id=None):
    households = Household.objects.all()
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
    householdWaterBill = currentNumberOfPeople.numberOfIndividuals*currentmonthlyBills.waterBill/totalNumberOfPeople

    # Current household refuse bill
    householdRefuseBill = currentmonthlyBills.refuseBill/Household.objects.all().count()

    # Current household electricity bill
    householdElectricityBill = householdPowerConsumed * currentmonthlyBills.electricityBill / householdAppliancesPowerConsumed
    
    # Household total bill for the month
    householdTotalBill = householdWaterBill + householdRefuseBill + householdElectricityBill

    print(householdTotalBill, householdWaterBill , householdRefuseBill , householdElectricityBill)


    Debt.objects.filter(dateOnBill__month=dateOnBill.month, dateOnBill__year=dateOnBill.year, household=Household.objects.get(id=household_id)).update(totalDept=householdTotalBill)


@receiver(post_save, sender=NumberOfIndividuals)
def my_handler(sender, instance, **kwargs):
    print(instance.dateOnBill, instance.household.user.id)

    if (checkparameters(dateOnBill=instance.dateOnBill,user_id=instance.household.user.id)):
        for household in Household.objects.all():
            updateBill(dateOnBill=instance.dateOnBill, household_id=household.id, user_id=instance.household.user.id)


@receiver(post_save, sender=MonthlyBill)
def my_handler(sender, instance, **kwargs):
    print(instance.dateOnBill, instance.user.id)

    if (checkparameters(dateOnBill=instance.dateOnBill,user_id=instance.user.id)):
        for household in Household.objects.all():
            updateBill(dateOnBill=instance.dateOnBill, household_id=household.id, user_id=instance.user.id)


@receiver(post_save, sender=HouseholdAppliance)
def my_handler(sender, instance, **kwargs):
    print(instance.dateOnBill, instance.household.user.id)

    if (checkparameters(dateOnBill=instance.dateOnBill,user_id=instance.household.user.id)):
        for household in Household.objects.all():
            updateBill(dateOnBill=instance.dateOnBill, household_id=household.id, user_id=instance.household.user.id)
