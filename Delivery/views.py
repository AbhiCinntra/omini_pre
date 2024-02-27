import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Employee.models import Employee
from Employee.serializers import EmployeeSerializer
from Delivery.models import DeliveryShipmentDetails
from Delivery.serializers import DeliveryShipmentSerializer

#Delivery Shipment Create API
@api_view(['POST'])
def createShipDetails(request):
    try:
        shippingName = request.data['shippingName']
        zipCode = request.data['zipCode']
        countryId = request.data['countryId']
        stateId = request.data['stateId']
        shippingType = request.data['shippingType']
        shippingAddress = request.data['shippingAddress']
        createDate = request.data['createDate']
        createTime = request.data['createTime']
        createdBy = request.data['createdBy']
        deliveryId = request.data['deliveryId']
        updateDate = request.data['updateDate']
        updateTime = request.data['updateTime']
        updateBy = request.data['updateBy']

        model = DeliveryShipmentDetails(shippingName=shippingName, zipCode=zipCode, countryId=countryId, stateId=stateId, shippingType=shippingType, shippingAddress = shippingAddress, createDate=createDate, createTime=createTime, createdBy=createdBy, deliveryId = deliveryId, updateDate =updateDate, updateTime=updateTime, updateBy=updateBy)
        
        model.save()
        
        return Response({"message": "successful", "status": "200", "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": "201", "data": []})

#Delivery Shipment All API
@api_view(["GET"])
def allShipDetails(request):
    log_obj = DeliveryShipmentDetails.objects.all().order_by("-id")
    result = showDeliveryShippingAddress(log_obj)
    return Response({"message": "Success","status": 200,"data":result})

#Delivery Shipment One API
@api_view(["POST"])
def oneShipDetails(request):
    try:
        id = request.data['id']
        if DeliveryShipmentDetails.objects.filter(pk=request.data['id']).exists():
            log_obj = DeliveryShipmentDetails.objects.filter(pk=request.data['id'])
            result = showDeliveryShippingAddress(log_obj)
            return Response({"message": "Success","status": 200,"data":result})
        else:
            return Response({"message": "Id Doesn't Exist", "status": 201, "data": []})
    except Exception as e:
        return Response({"message": str(e), "status": 201, "data": []})

#Delivery Shipment Update API
@api_view(['POST'])
def updateShipDetails(request):
    try:
        fetchid = request.data['id']
        model = DeliveryShipmentDetails.objects.get(pk = fetchid)
        model.shippingName = request.data['shippingName']
        model.zipCode = request.data['zipCode']
        model.countryId = request.data['countryId']
        model.stateId = request.data['stateId']
        model.shippingType = request.data['shippingType']
        model.shippingAddress = request.data['shippingAddress']
        model.updateDate = request.data['updateDate']
        model.updateTime = request.data['updateTime']
        model.updatedBy = request.data['updatedBy']
        model.deliveryId = request.data['deliveryId']

        model.save()

        return Response({"message":"successful","status":200,"data":[]})
    except:
        return Response({"message":"ID Wrong","status":201,"data":[]})
    
#Delivery Log Delete API
@api_view(['POST'])
def deleteLog(request):
    try:
        fetchids= request.data['id']
        for ids in fetchids:
            DeliveryShipmentDetails.objects.filter(pk=ids).delete()
            
        return Response({"message":"successful","status":"200","data":[]})   
    except:
        return Response({"message":"Id wrong","status":"201","data":[]})

#Delivery Shipment Details Data for all shipment and one shipment
def showDeliveryShippingAddress(objs):
    allShip = [];
    for obj in objs:
        createPerson = obj.createdBy  
        updatePerson = obj.updatedBy  
        
        ship_json = DeliveryShipmentSerializer(obj)
        finalShipData = json.loads(json.dumps(ship_json.data))
            
        if createPerson > 0:
            createPersonObj = Employee.objects.filter(pk = createPerson).values('id','firstName', 'lastName')
            createPersonjson = EmployeeSerializer(createPersonObj, many=True)
            if len(createPersonjson.data) > 0:
                finalShipData['createdBy'] = json.loads(json.dumps(createPersonjson.data[0]))   
            else:
                finalShipData['createdBy'] = []
        else:
            finalShipData['createdBy'] = []
            
        if updatePerson > 0:
            updatePersonObj = Employee.objects.filter(pk = updatePerson).values('id','firstName', 'lastName')
            updatePersonjson = EmployeeSerializer(updatePersonObj, many=True)
            if len(updatePersonjson.data) > 0:
                finalShipData['updatedBy'] = json.loads(json.dumps(updatePersonjson.data[0]))   
            else:
                finalShipData['updatedBy'] = []
        else:
            finalShipData['updatedBy'] = []
        
        allShip.append(finalShipData)
    return allShip

