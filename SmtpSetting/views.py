from django.shortcuts import render

from rest_framework.decorators import api_view    
from rest_framework import serializers
from rest_framework.response import Response

from SmtpSetting.models import SmtpSetting
from SmtpSetting.serializers import SmtpSettingSerializer

# Create Or Update SMTP Settings
@api_view(["POST"])
def smtp_settings(request):
    try:
        id = request.data['id']
        Host = request.data['Host'].strip()
        Port = request.data['Port'].strip()
        Sender = request.data['Sender'].strip()
        Password = request.data['Password'].strip()

        if id != "":
            smtpObj = SmtpSetting.objects.get(pk = id)
            smtpObj.Host = Host
            smtpObj.Port = Port
            smtpObj.Sender = Sender
            smtpObj.Password = Password
            smtpObj.save()
            return Response({"message": "Success","status": 200,"data":[]})
        else:
            if SmtpSetting.objects.filter(Sender = Sender).exists():
                return Response({"message": "Sender already exists:","status": 201,"data":[]})
            else:
                SmtpSetting(Host = Host, Port = Port, Sender = Sender, Password = Password ).save()        
                return Response({"message": "Success","status": 200,"data":[]})
    except Exception as e:
       return Response({"message": "error","status": 201,"data":[str(e)]})


# List SMTP Settings
@api_view(["GET"])
def all(request):
    try:
        settingObj = SmtpSetting.objects.all()
        settingJson = SmtpSettingSerializer(settingObj, many=True)

        return Response({"message": "Success","status": 200,"data":settingJson.data})
    except Exception as e:
       return Response({"message": "error","status": 201,"data":[str(e)]})
