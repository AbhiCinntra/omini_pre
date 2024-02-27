from django.urls import path,include
from .views import *

urlpatterns = [
    path('delivery/createShipDetails', createShipDetails),
    path('delivery/allShipDetails', allShipDetails),
    path('delivery/oneShipDetails', oneShipDetails),
    path('delivery/updateShipDetails', updateShipDetails),
]