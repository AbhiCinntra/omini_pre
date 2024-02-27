from django.urls import path,include
from .views import *

urlpatterns = [
    # Item
    path('discountpolicy/create', create),
    path('discountpolicy/all', all),
    # path('discountpolicy/update', update),
	# path('discountpolicy/one', one),
    # path('discountpolicy/delete', delete),
]
