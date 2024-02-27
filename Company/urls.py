from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('one',one),
    path('update', update),
    path('delete', delete),
    
    # Branches
    path('all_branches', all_branches),
]
