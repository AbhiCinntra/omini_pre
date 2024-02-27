from django.urls import path,include
from .views import *

urlpatterns = [
    
    path('all', all),
	path('one', one),
    path('all_filter', all_filter),
    path('all_filter_pagination', all_filter_pagination),

]
