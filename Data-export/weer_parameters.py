import requests
import time

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "EKrs0wMgD-h3nR8Jv6B5cv0va5-Vl4vpnBOlbxsexcFuMW5Grm3o2oH2VTZbZzaggfkgZJmkYpDPufxzp9ITjg=="
org = "deleite"
bucket = "deleite"

client = InfluxDBClient(url="http://51.210.255.2:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

#ID BRUGGE = 2800930
BASE = "https://api.openweathermap.org/data/2.5/weather?id=2800930&appid=3307bc7ab88cf7bddd795d387181b809"

while True:
    Get = requests.get(BASE)
    Get =  Get.json()
    temp = round(Get.get("main").get('temp') - 273.15,2)
    print(temp)
    sequence = ["Meter,Temp=Temp Celsius={}".format(temp)]  
    write_api.write(bucket, org, sequence)
    time.sleep(60)
