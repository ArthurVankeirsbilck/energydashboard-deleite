from O365 import Account, MSGraphProtocol, FileSystemTokenBackend
import mysql.connector
from datetime import datetime
import time
import math
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import requests

# You can generate a Token from the "Tokens Tab" in the UI
token = "EKrs0wMgD-h3nR8Jv6B5cv0va5-Vl4vpnBOlbxsexcFuMW5Grm3o2oH2VTZbZzaggfkgZJmkYpDPufxzp9ITjg=="
org = "deleite"
bucket = "deleite"

client = InfluxDBClient(url="http://51.210.255.2:8086", token=token)
query_api = client.query_api()

credentials = ('77c9fda0-18e0-40af-8d84-d100304b2906', 'w7f7Q~EMY6rkpAWL9Gv4gEXGfT1s1X.uBM8YF')

mydb = mysql.connector.connect(
  host="51.210.255.2",
  user="root",
  password="appelflap",
  database="deleite"
)
mycursor = mydb.cursor()
protocol = MSGraphProtocol() 
token_backend = FileSystemTokenBackend(token_path='token', token_filename='my_token.txt')  
# refresh =  LockableFileSystemTokenBackend(FileSystemTokenBackend)
# refresh.should_refresh_token(con=True)

#protocol = MSGraphProtocol(defualt_resource='<sharedcalendar@domain.com>') 

def Average(lst):
    return (sum(lst) / len(lst))/60

results = []
while True:
   account = Account(credentials, token_backend=token_backend)
   scopes = ['offline_access', 'Calendars.Read']
   # if account.authenticate(scopes=scopes):
   #    print('Authenticated!')
   # print(account.is_authenticated)


   schedule = account.schedule()
   calendar = schedule.get_default_calendar()
   events = calendar.get_events(include_recurring=False) 
   #events = calendar.get_events(query=q, include_recurring=True) 

   for event in events:
      mycursor = mydb.cursor()
      try:
         start_str = str(event.start)
         stop_str = str(event.end)
         start = datetime.strptime(start_str[:-6], '%Y-%m-%d %H:%M:%S')
         stop = datetime.strptime(stop_str[:-6], '%Y-%m-%d %H:%M:%S')
         start_unixtime = math.trunc(time.mktime(start.timetuple()))
         print(start_str[:-6])
         stop_unixtime = math.trunc(time.mktime(stop.timetuple()))
         query = requests.get("http://51.210.255.2:5000/Data/{}/{}/Meter/Smappee1/Verbruik/NetL1".format(start_unixtime, stop_unixtime))
         query2 = requests.get("http://51.210.255.2:5000/Data/{}/{}/Meter/Smappee1/Verbruik/NetL2".format(start_unixtime, stop_unixtime))
         query3 = requests.get("http://51.210.255.2:5000/Data/{}/{}/Meter/Smappee1/Verbruik/NetL3".format(start_unixtime, stop_unixtime))
         results = list(query.json())
         results.extend(list(query2.json()))
         results.extend(list(query3.json()))
         if sum(results) == 0:
            print("No data.")
         else:
            sql = "INSERT INTO deleite.agenda (Datum, Name, UUID, Value, Time) VALUES('{}', '{}', '{}', '{}', '{}');".format(start_str[:-6]+" TOT "+stop_str[:-6] , event.subject + " / " +start_str[:-6]+" TOT "+stop_str[:-6], str(event.ical_uid), (sum(results))/60, datetime.now())
            mycursor.execute(sql)
            mydb.commit()
         results.clear()
      except mysql.connector.errors.IntegrityError:
         print("Value already in database.")
   time.sleep(300)
      










      