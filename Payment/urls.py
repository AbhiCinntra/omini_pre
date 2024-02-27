from django.urls import path,include
from .views import *

urlpatterns = [
    path('payment/create', create),
    path('payment/all', all),
    path('payment/one', one),
    path('payment/update', update),
    path('payment/delete', delete),
    path('payment/payment_img_delete', payment_img_delete),
]
