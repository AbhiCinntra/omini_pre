from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('all_filter', all_filter),
	path('one', one),
    path('update', update),
    path('delete', delete),
    # path('inventory_create',inventory_create),
    # path('inventory_one',inventory_one)
]
