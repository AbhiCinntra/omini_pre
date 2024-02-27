from django.urls import path,include
from .views import *

urlpatterns = [
    path('smtp/create', smtp_settings),
    path('smtp/all', all)
]
