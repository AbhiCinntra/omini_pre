import mysql.connector
import calendar
import requests, json
import time
import math
from datetime import date, datetime
import sys, os

def none(inp):
    inp = str(inp)
    if inp.lower()=="none":
        return "";
    else:
        return inp

currentDate = date.today()
currentDay = calendar.day_name[currentDate.weekday()]  # this will return the day of a week
currentTime = datetime.today().strftime("%I:%M %p")
currentDateTime = f"{currentDate} {currentTime}"
serverDateTime = datetime.now()

print("Today date is: ", currentDate)
print("Today day is: ", currentDay)
print("Today Current time: ", currentTime)
print("Today Current serverDateTime: ", serverDateTime)

businessPartnerBP ="http://43.204.160.245:8001/businesspartner/syncbp"
r = requests.get(businessPartnerBP)
print(r.text)