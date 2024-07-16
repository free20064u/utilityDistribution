
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('utilityBills/', views.utilityBillsView, name='utilityBills'),
    path('bills/', views.billsView, name='bills'),
    path('editBill/<int:id>', views.editBillView, name='editBill'),
]
