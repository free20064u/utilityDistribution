
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('utilityBills/', views.utilityBillsView, name='utilityBills'),
    path('bills/', views.billsView, name='bills'),
    path('editBill/<int:id>/', views.editBillView, name='editBill'),
    path('household/', views.householdView, name='household'),
    path('addHousehold/', views.addHouseholdView, name='addHousehold'),
    path('editHousehold/<int:id>/', views.editHouseholdView, name='editHousehold'),
    path('electricalAppliance/', views.electricalApplianceView, name='electricalAppliance'),
    path('addAppliance/', views.addApplianceView, name='addAppliance'),
    path('editAppliance/<int:id>/', views.editApplianceView, name='editAppliance'),
    path('profile/<int:id>/', views.profileView, name='profile'),
    path('addHouseholdAppliance/<int:id>/', views.addHouseholdApplianceView, name='addHouseholdAppliance'),
    path('payBill/<int:id>/', views.payBillView, name='payBill'),
    path('addPeople/<int:id>/', views.addPeopleView, name='addPeople'),
    path('editNoOfPeople/<int:id>/', views.editNoOfPeopleView, name='editNoOfPeople'),
    path('update/', views.webhook, name='update'),
    path('docs', views.docsView, name='docs'),
    path('contact', views.contactView, name='contact')
 ]
