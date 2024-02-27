from .models import *
from Employee.models import Employee

import requests, json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *

from pytz import timezone
from datetime import datetime as dt

date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')

@api_view(['GET'])
def price_list_all(request):
    try:
        # priceListObj = PriceList.objects.all().order_by("-id")
        priceListObj = PriceList.objects.all().order_by("id")
        priceListJson = PriceListSerializer(priceListObj, many=True)
        return Response({"message":"successful","status":200,"data": priceListJson.data})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

