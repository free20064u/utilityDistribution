from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Appliance(models.Model):
    date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100)
    power = models.CharField(max_length=10)


class Household(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateField(auto_now_add=True)


class UtilBill(models.Model):
    dateAdded = models.DateTimeField(auto_now_add=True)
    billDate = models.DateField()
    dustbinBill = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    electricBill = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    waterBill = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

