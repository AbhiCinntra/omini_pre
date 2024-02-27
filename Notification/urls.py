from django.urls import path,include
from .views import *

urlpatterns = [
    path('all', all),
    path('one', one),
    path('read', read),
    path('delete', delete)
]
