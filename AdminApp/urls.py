
from django.urls import path
from AdminApp import views

urlpatterns = [
    path('', views.index),
    path('AdminAction', views.AdminAction),
    path('AdminHome', views.AdminHome),
    path('loaddataset', views.loaddataset),
    path('preprocess', views.preprocess),
    path('runSVM', views.runSVM),
    path('runRF', views.runRF),
    path('runComparison', views.runComparison),
]
