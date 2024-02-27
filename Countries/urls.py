from django.urls import path,include
from .views import *
from Countries import views, viewsStates

urlpatterns = [
    path('countries/all', views.all),
    path('states/all', viewsStates.all),
    path('states/create', viewsStates.create)
]
