# http://103.107.67.160:8002/item/sync_inventroy
import requests, json
import time
import math
import mysql.connector

import sys, os
from datetime import datetime
from datetime import date, datetime, timedelta
import calendar

syncUrl = "http://103.107.67.160:8002/item/sync_inventroy"
res = requests.get(syncUrl, verify=False)
print(res.text)