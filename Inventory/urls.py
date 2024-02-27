from django.urls import path,include
from .views import *

urlpatterns = [
    path('create', create),
    path('all', all),
    path('all_filter', all_filter),
	path('delivery', delivery),
	path('one',one),
    path('update',update)
]
