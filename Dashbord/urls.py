from django.contrib import admin
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.form1, name="form1"),
    path('form2/', views.form2, name="form2"),
    path('formsubmit', csrf_exempt(views.formsubmit), name="formsubmit"),
    path('form3/', views.form3, name="form3"),
    path('form4/', views.form4, name="form4"),
    path('form5/', views.form5, name="form5"),
    path('pay', views.pay, name="pay"),
    # path('pay_ment/', views.call_back_url, name="payment"),
]
