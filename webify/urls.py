from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'webify'

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard-home', views.dashboard, name="dashboard"),
    path('projects', views.projects, name="projects"),
    path('server', views.server, name="server"),
    path('bank', views.bank, name="bank"),
    path('wallet', views.wallet, name="wallet"),
    path('payment/', views.call_back_url, name="payment"),
    path('pay', views.pay, name="pay"),
    path('transfermoney', views.transfermoney, name="transfermoney"),
    path('wallettransfer', views.wallettransfer, name="wallettransfer"),
    path('forum', views.forum, name="forum"),
    path("like/<id>/", views.liked_qustion, name="liked_qustion"),
    path("user_comment/<id>", views.question_comment, name="question_comment"),
    path("inventory/", views.Inventory, name="Inventory"),
    # path("dislike/<id>/", views.dislike_qustion, name="dislike_qustion"),
    path('forum-details/<id>/', views.forum_details, name="forum_details"),
]
