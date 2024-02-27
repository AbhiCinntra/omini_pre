from .models import *
from rest_framework.decorators import api_view    
from rest_framework.response import Response
from .serializers import *

from pytz import timezone
from datetime import datetime as dt

date = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d')
yearmonth = dt.now(timezone("Asia/Kolkata")).strftime('%Y-%m')
time = dt.now(timezone("Asia/Kolkata")).strftime('%H:%M %p')


# Create your views here.  
#Warehouse Create API
@api_view(['POST'])
def create(request):
    if Warehouse.objects.filter(WarehouseName = request.data['WarehouseName']).exists():
        return Response({"message":"Already exist Name","status":"409","data":[]})
    else:
        try:
            BusinessPlaceID = request.data['BusinessPlaceID']
            Location = request.data['Location']
            WarehouseCode = request.data['WarehouseCode']
            WarehouseName = request.data['WarehouseName']
            Block = request.data['Block']
            State = request.data['State']
            City = request.data['City']
            Country = request.data['Country']
            County = request.data['County']
            Street = request.data['Street']
            ZipCode = request.data['ZipCode']
            Inactive = request.data['Inactive']
            CreatedDate = request.data['CreatedDate']
            UpdatedDate = request.data['UpdatedDate']
            
            model = Warehouse(BusinessPlaceID = BusinessPlaceID,Location = Location,WarehouseCode = WarehouseCode,WarehouseName = WarehouseName,Block = Block,State = State,City = City,Country = Country,County = County,Street = Street,ZipCode = ZipCode,Inactive = Inactive,CreatedDate = CreatedDate,UpdatedDate = UpdatedDate)
            
            model.save()
            w = Warehouse.objects.latest('id')
            return Response({"message":"successful","status":200,"data":[{"id":w.id}]})
        except Exception as e:
            return Response({"message":str(e),"status":201,"data":[]})

#Warehouse Update API
@api_view(['POST'])
def update(request):
    fetchid = request.data['id']
    try:
        model = Warehouse.objects.get(pk = fetchid)
        model = request.data['WarehouseName']
        model = request.data['Block']
        model = request.data['State']
        model = request.data['City']
        model = request.data['Country']
        model = request.data['County']
        model = request.data['Street']
        model = request.data['ZipCode']
        model = request.data['Inactive']
        model.save()
        
        return Response({"message":"successful","status":200, "data":[request.data]})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#Warehouse All API
@api_view(["GET"])
def all(request):
    try:
        Warehouses_obj = Warehouse.objects.all().order_by("-id")
        allwr = WarehouseSerializer(Warehouses_obj, many=True)
        return Response({"message": "Success","status": 200,"data":allwr.data})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#Warehouse All filter API
@api_view(["POST"])
def all_filter(request):
    try:
        BusinessPlaceID = request.data['BusinessPlaceID']
        Warehouses_obj = Warehouse.objects.filter(BusinessPlaceID = BusinessPlaceID, Inactive = "tNO").values("BusinessPlaceID","WarehouseCode","WarehouseName")
        allwr = WarehouseSerializer(Warehouses_obj, many=True)
        return Response({"message": "Success","status": 200,"data":allwr.data})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#Warehouse One API
@api_view(["POST"])
def one(request):
    try:
        id=request.data['id']    
        Warehouses_obj = Warehouse.objects.get(id=id)    
        allwr = WarehouseSerializer(Warehouses_obj, many=False)
        return Response({"message": "Success","status": 200,"data":allwr.data})
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

#Warehouse delete
@api_view(['POST'])
def delete(request):
    try:
        fetchid=request.data['id']
        fetchdata=Warehouse.objects.filter(pk=fetchid).delete()
        return Response({"message":"successful","status":"200","data":[]})        
    except Exception as e:
        return Response({"message":str(e),"status":201,"data":[]})

# #Inventory Create API
# @api_view(['POST'])
# def inventory_create(request):
#     try:
#         ItemCode = request.data['ItemCode']
#         WarehouseID = request.data['WarehouseID']
#         Add = int(request.data['Add'])
#         Remove = int(request.data['Remove'])
#         Type = request.data['Type']
#         Emp = request.data['Emp']
#         Remark = request.data['Remark']
#         CreatedDate = request.data['CreatedDate']
#         CreatedTime = request.data['CreatedTime']
        
#         if Add > 0 and Remove > 0:
#             return Response({"message":"successful","status":201,"data":[{"Error":"Please select one Add or Remove"}]})
        
#         Inventory_obj = Inventory.objects.filter(ItemCode=ItemCode, WarehouseID=WarehouseID).order_by("-id")[:1]
#         if len(Inventory_obj) < 1:
#             invt = 0
#         else:
#             for inv in Inventory_obj:
#                 invt = inv.Inventory
            
#         if Remove > invt:
#             msg = "Inventory should be less than stock: Inventory:"+str(invt)+" and Remove:"+str(Remove)
        
#             return Response({"message":msg, "status":201, "data":[]})
        
#         if Add > 0:
#             invt = invt + Add
#         elif Remove > 0:
#             invt = invt - Remove            
#         else:
#             return Response({"message":"successful","status":201,"data":[{"Error":"Something went wrong"}]})
        
#         model = Inventory(ItemCode = ItemCode, WarehouseID = WarehouseID, Add = Add, Remove = Remove, Inventory = invt, Type = Type, Emp  = Emp, Remark = Remark, CreatedDate = CreatedDate, CreatedTime = CreatedTime)        
#         model.save()
        
#         invt_obj = Inventory.objects.latest('id')
#         print(invt_obj.Inventory)
        
#         return Response({"message":"successful","status":200,"data":[{"Inventory":invt_obj.Inventory}]})
#     except Exception as e:
#         return Response({"message":"Not Created","status":201,"data":[{"Error":str(e)}]})

# #Inventory All API
# @api_view(["POST"])
# def inventory_one(request):
#     ItemCode = request.data['ItemCode']
#     WarehouseID = request.data['WarehouseID']
#     Inventory_obj = Inventory.objects.filter(ItemCode=ItemCode, WarehouseID=WarehouseID).order_by("-id")[:1]
#     inv = InventorySerializer(Inventory_obj, many=True)
#     return Response({"message": "Success","status": 200,"data":inv.data})
