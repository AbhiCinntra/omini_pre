import requests, json
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="standalone_pre"
)
mycursor = mydb.cursor(dictionary=True)
#print("test comment")


# class Config:
  # def __init__(self):
    # mycursor.execute("select * from Appsetting_appsetting")
    # obj = mycursor.fetchall()
    # self.sap = json.loads(obj[0]['Data'])
    # self.sql = json.loads(obj[1]['Data'])

# config = Config()
# print(config.sap)
# print(config.sql)
