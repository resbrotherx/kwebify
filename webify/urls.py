from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('bank', views.bank, name="bank"),
]
