
from django.urls import path
from UserApp import views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('RegAction', views.RegAction),
    path('Userction', views.Userction),
    path('UserHome', views.UserHome),
    path('predictchurn', views.predictchurn),
    path('PredAction', views.PredAction),
]
