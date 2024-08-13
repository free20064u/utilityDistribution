from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Household(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entryDate = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return self.name


class NumberOfIndividuals(models.Model):
    numberOfIndividuals = models.IntegerField()
    entryDate = models.DateField(auto_now_add=True)
    dateOnBill = models.DateField()
    household = models.ForeignKey(Household, on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.household} -- {self.numberOfIndividuals}')
    
    # Total number of people in all the house hold for a particular month
    def totalNumberOfPeopel(self, month=None, year=None):
        totalMembers=0
        households = NumberOfIndividuals.objects.filter(dateOnBill__month=month, dateOnBill__year=year)
        for household in households:
            totalMembers += int(household.numberOfIndividuals)
        return totalMembers


class Debt(models.Model):
    totalDept = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    entryDate = models.DateField(auto_now_add=True)
    dateOnBill = models.DateField()
    household = models.ForeignKey(Household, on_delete=models.CASCADE)

    def householdTotalDebt(self, household_id=None):
        total = 0
        debts = Debt.objects.filter(household_id=household_id)
        for debt in debts:
            total += debt.totalDept

        return total

    
class Payment(models.Model):
    entryDate = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    household = models.ForeignKey(Household, on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.household} --- {self.amount}')
    
    def householdTotalPayment(self, household_id=None):
        total = 0
        payments = Payment.objects.filter(household_id=household_id)
        for payment in payments:
            total += payment.amount

        return total


class MonthlyBill(models.Model):
    entryDate = models.DateTimeField(auto_now_add=True)
    dateOnBill = models.DateField()
    refuseBill = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    electricityBill = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    waterBill = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def totalBill(self):
        bill = self.refuseBill + self.electricityBill + self.waterBill
        return (bill)
    
    def __self__(self):
        return (f'{self.entryDate} -- {self.refuseBill} -- {self.electricityBill} -- {self.waterBill}')

    
class Appliance(models.Model):
    entryDate = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100)
    power = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.name} -- {self.power}W')


class HouseholdAppliance(models.Model):
    entryDate = models.DateField(auto_now_add=True)
    dateOnBill = models.DateField()
    quantity = models.IntegerField(default=0)
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    appliance = models.ForeignKey(Appliance, on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.household} -- {self.appliance}')
    

    def totalPower(self):
        total = self.appliance.power * self.quantity
        return total
