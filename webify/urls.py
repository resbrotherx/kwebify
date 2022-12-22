from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('bank', views.bank, name="bank"),
    path('wallet', views.wallet, name="wallet"),
    path('payment/', views.call_back_url, name="payment"),
    path('pay', views.pay, name="pay"),
    path('transfermoney', views.transfermoney, name="transfermoney"),
]
