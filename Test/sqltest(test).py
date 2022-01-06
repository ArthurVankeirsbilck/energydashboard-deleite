import mysql.connector
import time
from datetime import datetime
import math

mydb = mysql.connector.connect(
  host="51.210.255.2",
  user="root",
  password="appelflap",
  database="deleite"
)

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "rp85Xigw4RQk4FfFyRSHZZvHoZYPIRble002bUxieV4Z6e6Q9Lv9fEphyzLQB6czGGNX6wdvgQm0ZB2gah316g=="
org = "hulstenhof"
bucket = "hulstenhof"

client = InfluxDBClient(url="http://54.36.101.197:8086", token=token)
query_api = client.query_api()

mycursor = mydb.cursor()

mycursor.execute("SELECT ID, Datum, Name, DatumEnd, UUID FROM deleite.agenda;")
results = []
myresult = mycursor.fetchall()

for x in myresult:
    start = datetime.strptime(x[1][:-6], '%Y-%m-%d %H:%M:%S')
    stop = datetime.strptime(x[3][:-6], '%Y-%m-%d %H:%M:%S')
    start_unixtime = math.trunc(time.mktime(start.timetuple()))
    stop_unixtime = math.trunc(time.mktime(stop.timetuple()))
    print(start_unixtime)
    query = 'from(bucket: "hulstenhof") |> range(start: {}, stop: {}) |> filter(fn: (r) => r["_measurement"] == "Boiler Klein") |> filter(fn: (r) => r["Meter"] == "teller-1") |> filter(fn: (r) => r["_field"] == "ConsumtionW")'.format(start_unixtime, stop_unixtime)
    result = query_api.query(org=org, query=query)
    for table in result:
        for record in table.records:
            results.append(record.get_value())
    print(datetime.now())
    print(results)
    results.clear()
