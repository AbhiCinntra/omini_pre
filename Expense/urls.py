from django.urls import path,include
from .views import *


urlpatterns = [
    path('expense/create', create),
    path('expense/all', all),
    path('expense/one', one),
    path('expense/update', update),
    path('expense/delete', delete),
    path('expense/expense_img_delete', expense_img_delete),
]