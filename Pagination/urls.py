from django.urls import path
from .views import *

urlpatterns = [
    path('pagination/create', create),
    path('pagination/all', all)
]
