from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('signOut/', views.signOutView, name='signOut'),
    path('register/', views.registerView, name='register'),
    path('editUserPic/<int:id>/', views.editUserPicView, name='editUserPic'),
    path('editUserDetail/<int:id>/', views.editUserDetailView, name='editUserDetail'),
]
