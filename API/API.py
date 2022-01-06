from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)
token = "EKrs0wMgD-h3nR8Jv6B5cv0va5-Vl4vpnBOlbxsexcFuMW5Grm3o2oH2VTZbZzaggfkgZJmkYpDPufxzp9ITjg=="
org = "deleite"
bucket = "deleite"
client = InfluxDBClient(url="http://51.210.255.2:8086", token=token)

class Data(Resource):
    def get(self, results, start, stop, inst, meter, teller, ver):
        query = 'from(bucket: "deleite")|> range(start: {}, stop: {})|> filter(fn: (r) => r["_measurement"] == "{}")|> filter(fn: (r) => r["{}"] == "{}")|> filter(fn: (r) => r["_field"] == "{}")'.format(start, stop, inst, meter, teller, ver)
        result = client.query_api().query(query, org=org)
        results = []
        for table in result:
            for record in table.records:
                results.append('{}'.format(record.get_value()))
        return results
        
class Prijs(Resource):
    def post(self, results):
        print(request.form['elektriciteitsprijs'])
        return "Elektriciteitsprijs posted: {}".format(request.form['elektriciteitsprijs'])

api.add_resource(Data, "/<string:results>/<string:start>/<string:stop>/<string:inst>/<string:meter>/<string:teller>/<string:ver>")
api.add_resource(Prijs, "/<string:results>")

if __name__ ==  "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) 
