from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name="signup"),
    path('create', views.create, name="create"),
    path("Verify-otp/",views.Verify_otp, name="Verify-otp"),
    path("send_otp",views.send_otp,name="send_otp"),
    path("Welcome/",views.thanku, name="thanku"),
    path("status_verify/",views.status_verify, name="status_verify"),
    path("onbording",views.Onbording, name="onbording"),
    
    
]
