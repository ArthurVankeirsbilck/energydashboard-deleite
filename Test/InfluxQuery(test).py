from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "rp85Xigw4RQk4FfFyRSHZZvHoZYPIRble002bUxieV4Z6e6Q9Lv9fEphyzLQB6czGGNX6wdvgQm0ZB2gah316g=="
org = "hulstenhof"
bucket = "hulstenhof"

client = InfluxDBClient(url="http://54.36.101.197:8086", token=token)

query = f'from(bucket: "hulstenhof")|> range(start: -30m, stop: now())|> filter(fn: (r) => r["_measurement"] == "consumption")|> filter(fn: (r) => r["Meter"] == "teller-1")|> filter(fn: (r) => r["_field"] == "ConsumtionW")'
result = client.query_api().query(query, org=org)

results = []
for table in result:
    for record in table.records:
        results.append(record.get_value())

print(results)