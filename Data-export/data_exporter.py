import random
from paho.mqtt import client as mqtt_client
import json
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time

token = "EKrs0wMgD-h3nR8Jv6B5cv0va5-Vl4vpnBOlbxsexcFuMW5Grm3o2oH2VTZbZzaggfkgZJmkYpDPufxzp9ITjg=="
org = "deleite"
bucket = "deleite"
client = InfluxDBClient(url="http://51.210.255.2:8086", token=token)
elektriciteit = 0.475
elektriciteitEUR = 0.25
write_api = client.write_api(write_options=SYNCHRONOUS)

def aggregate(value, lijst):
    if len(lijst) < 1:
        lijst.append(value)
    else:
        Average = sum(lijst) / len(lijst)
        lijst.clear()
        return Average

def CO2_omrekenen(brandstof, verbruik):
    CO2 = (((verbruik/3600)/1000)*brandstof)
    return CO2

def Euro_omrekenen(brandstof, verbruik):
    Euro = (((verbruik/3600)/1000)*brandstof)
    return Euro

def Zv(verbruik, productie):
    if verbruik - productie < 0:
        Import = 0
    else:
        Import = verbruik - productie
    Zc = round(((verbruik - Import)/verbruik)*100,2)
    return Zc

def Zc(verbruik, productie):
    if productie - verbruik < 0:
        export = 0
    else:
        export = productie - verbruik
    Zv = round(((productie-export)/productie)*100,2)
    return Zv


broker = '51.210.255.2'
port = 1883
topic = "servicelocation/282229d1-9fb3-401b-9444-0b74495882e9/realtime"
topic2 = "servicelocation/5b551b18-04fd-44b5-a545-15885334703d/realtime"
client_id = f'python-mqtt-{random.randint(0, 100)}' #random id
def connect_mqtt() -> mqtt_client:

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

list_totalPower = []
list_L1 = []
list_L2 = []
list_L3 = []
list_StoomktlL1 = []
list_StoomktlL2 = []
list_StoomktlL3 = []
list_BottelarijL1 = []
list_BottelarijL2 = []
list_BottelarijL3 = []
list_BordenCDL1 = []
list_BordenCDL2 = []
list_BordenCDL3 = []
list_SolarL1 = []
list_SolarL2 = []
list_SolarL2 = []
list_SolarL3 = []
list_CompressorL1 = []
list_CompressorL2 = []
list_CompressorL3 = []
list_BrouwinstallatieL1 = []
list_BrouwinstallatieL2 = []
list_BrouwinstallatieL3 = []
list_VoedingsbordEL1 = []
list_VoedingsbordEL2 = []
list_VoedingsbordEL3 = []
List_KoelcelL1 = []
List_KoelcelL2 = []
List_KoelcelL3 = []
list_Bordb_wc_L1 = []
list_Bordb_wc_L2 = []
list_Bordb_wc_L3 = []
list_MonoFL1 = []
list_MonoFL2 = []
list_MonoFL3 = []

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        if msg.topic == 'servicelocation/282229d1-9fb3-401b-9444-0b74495882e9/realtime':
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            my_dict = msg.payload.decode()
            my_dict = json.loads(my_dict)

            totalPower = aggregate(my_dict.get("totalPower"), list_totalPower)
            NetL1 = aggregate(my_dict.get("channelPowers")[0].get('power'), list_L1)
            NetL2 = aggregate(my_dict.get("channelPowers")[1].get('power'), list_L2)
            NetL3 = aggregate(my_dict.get("channelPowers")[2].get('power'), list_L3)

            StoomktlL1 = aggregate(my_dict.get("channelPowers")[3].get('power'), list_StoomktlL1)
            StoomktlL2 = aggregate(my_dict.get("channelPowers")[4].get('power'), list_StoomktlL2)
            StoomktlL3 = aggregate(my_dict.get("channelPowers")[5].get('power'), list_StoomktlL3)

            BottelarijL1 = aggregate(my_dict.get("channelPowers")[6].get('power'), list_BottelarijL1)
            BottelarijL2 = aggregate(my_dict.get("channelPowers")[7].get('power'), list_BottelarijL2)
            BottelarijL3 = aggregate(my_dict.get("channelPowers")[8].get('power'), list_BottelarijL3)

            BordenCDL1 = aggregate(my_dict.get("channelPowers")[9].get('power'), list_BordenCDL1)
            BordenCDL2 = aggregate(my_dict.get("channelPowers")[10].get('power'), list_BordenCDL2)
            BordenCDL3 = aggregate(my_dict.get("channelPowers")[11].get('power'), list_BordenCDL3)

            SolarL1 = aggregate(my_dict.get('channelPowers')[12].get('power'), list_SolarL1)
            SolarL2 = aggregate(my_dict.get('channelPowers')[13].get('power'), list_SolarL2)
            SolarL3 = aggregate(my_dict.get('channelPowers')[14].get('power'), list_SolarL3)

            CompressorL1 = aggregate(my_dict.get('channelPowers')[15].get('power'), list_CompressorL1)
            CompressorL2 = aggregate(my_dict.get('channelPowers')[16].get('power'), list_CompressorL2)
            CompressorL3 = aggregate(my_dict.get('channelPowers')[17].get('power'), list_CompressorL3)

            BrouwinstallatieL1 = aggregate(my_dict.get('channelPowers')[18].get('power'), list_BrouwinstallatieL1)
            BrouwinstallatieL2 = aggregate(my_dict.get('channelPowers')[19].get('power'), list_BrouwinstallatieL2)
            BrouwinstallatieL3 = aggregate(my_dict.get('channelPowers')[20].get('power'), list_BrouwinstallatieL3)

            VoedingsbordEL1 = aggregate(my_dict.get('channelPowers')[21].get('power'), list_VoedingsbordEL1)
            VoedingsbordEL2 = aggregate(my_dict.get('channelPowers')[22].get('power'), list_VoedingsbordEL2)
            VoedingsbordEL3 = aggregate(my_dict.get('channelPowers')[23].get('power'), list_VoedingsbordEL3)

            if totalPower != None:
                NetTot = NetL1 + NetL2 + NetL3
                NetTotEuro = Euro_omrekenen(elektriciteit, NetTot)
                NetTotCO2 = CO2_omrekenen(elektriciteit, NetTot)

                VoedingsbordETot = VoedingsbordEL1 + VoedingsbordEL2 + VoedingsbordEL3
                VoedingsbordEtot_CO2 = CO2_omrekenen(elektriciteit, VoedingsbordETot)

                BrouwinstallatieTot = BrouwinstallatieL1 + BrouwinstallatieL2 + BrouwinstallatieL3
                BrouwinstallatieTot_CO2 = CO2_omrekenen(elektriciteit,BrouwinstallatieTot)    

                CompressorTot = CompressorL1 + CompressorL2 + CompressorL3
                CompressorTot_CO2 = CO2_omrekenen(elektriciteit, CompressorTot)

                SolarTot = SolarL1 + SolarL2 +SolarL3
                SolarTot_CO2 = CO2_omrekenen(elektriciteit, SolarTot)*-1

                BordenCDTot = BordenCDL1 + BordenCDL2 + BordenCDL3
                BordenCDTot_CO2 = CO2_omrekenen(elektriciteit, BordenCDTot)

                BottelarijTot = BottelarijL1 + BottelarijL2 + BottelarijL3
                BottelarijTot_CO2 = CO2_omrekenen(elektriciteit, BottelarijTot)
                
                StoomktlTot = StoomktlL1 + StoomktlL2 + StoomktlL3
                StoomktlTot_CO2 = CO2_omrekenen(elektriciteit, StoomktlTot)

                Zelfconsumptie = Zc(totalPower, SolarTot)
                Zelfvoorziening = Zv(totalPower, SolarTot)

                sequence = [
                #Elektriciteit
                "Meter,Smappee1=Verbruik Zc={}".format(Zelfconsumptie),
                "Meter,Smappee1=Verbruik Zv={}".format(Zelfvoorziening),
                "Meter,Smappee1=Verbruik NetL1={}".format(NetL1),
                "Meter,Smappee1=Verbruik NetL2={}".format(NetL2),
                "Meter,Smappee1=Verbruik NetL3={}".format(NetL3),
                "Meter,Smappee1=Verbruik StoomktlL1={}".format(StoomktlL1),
                "Meter,Smappee1=Verbruik StoomktlL2={}".format(StoomktlL2),
                "Meter,Smappee1=Verbruik StoomktlL3={}".format(StoomktlL3),
                "Meter,Smappee1=Verbruik BottelarijL1={}".format(BottelarijL1),
                "Meter,Smappee1=Verbruik BottelarijL2={}".format(BottelarijL2),
                "Meter,Smappee1=Verbruik BottelarijL3={}".format(BottelarijL3),
                "Meter,Smappee1=Verbruik BordenCDL1={}".format(BordenCDL1),
                "Meter,Smappee1=Verbruik BordenCDL2={}".format(BordenCDL2),
                "Meter,Smappee1=Verbruik BordenCDL3={}".format(BordenCDL3),
                "Meter,Smappee1=Verbruik SolarL1={}".format(SolarL1),
                "Meter,Smappee1=Verbruik SolarL2={}".format(SolarL2),
                "Meter,Smappee1=Verbruik SolarL3={}".format(SolarL3),
                "Meter,Smappee1=Verbruik CompressorL1={}".format(CompressorL1),
                "Meter,Smappee1=Verbruik CompressorL2={}".format(CompressorL2),
                "Meter,Smappee1=Verbruik CompressorL3={}".format(CompressorL3),
                "Meter,Smappee1=Verbruik BrouwinstallatieL1={}".format(BrouwinstallatieL1),
                "Meter,Smappee1=Verbruik BrouwinstallatieL2={}".format(BrouwinstallatieL2),
                "Meter,Smappee1=Verbruik BrouwinstallatieL3={}".format(BrouwinstallatieL3),
                "Meter,Smappee1=Verbruik VoedingsbordEL1={}".format(VoedingsbordEL1),
                "Meter,Smappee1=Verbruik VoedingsbordEL2={}".format(VoedingsbordEL2),
                "Meter,Smappee1=Verbruik VoedingsbordEL3={}".format(VoedingsbordEL3),

                #CO2
                "Meter,Smappee1=CO2 VoedingsbordEtot_CO2={}".format(VoedingsbordEtot_CO2),
                "Meter,Smappee1=CO2 BrouwinstallatieTot_CO2={}".format(BrouwinstallatieTot_CO2),
                "Meter,Smappee1=CO2 CompressorTot_CO2={}".format(CompressorTot_CO2), 
                "Meter,Smappee1=CO2 SolarTot_CO2={}".format(SolarTot_CO2),
                "Meter,Smappee1=CO2 BordenCDTot_CO2={}".format(BordenCDTot_CO2),
                "Meter,Smappee1=CO2 BottelarijTot_CO2={}".format(BottelarijTot_CO2),
                "Meter,Smappee1=Euro NetTot={}".format(NetTotEuro),
                "Meter,Smappee1=CO2 NetTot_CO2={}".format(NetTotCO2)
                ]        
                write_api.write(bucket, org, sequence)

        else:
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            my_dict = msg.payload.decode()
            my_dict = json.loads(my_dict)
            
            KoelcelL1 = aggregate(my_dict.get("channelPowers")[0].get('power'), List_KoelcelL1)
            KoelcelL2 = aggregate(my_dict.get("channelPowers")[1].get('power'), List_KoelcelL2)
            KoelcelL3 = aggregate(my_dict.get("channelPowers")[2].get('power'), List_KoelcelL3)

            Bordb_wc_L1 = aggregate(my_dict.get("channelPowers")[3].get('power'), list_Bordb_wc_L1)
            Bordb_wc_L2 = aggregate(my_dict.get("channelPowers")[4].get('power'), list_Bordb_wc_L2)
            Bordb_wc_L3 = aggregate(my_dict.get("channelPowers")[5].get('power'), list_Bordb_wc_L3)

            MonoFL1 = aggregate(my_dict.get("channelPowers")[6].get('power'), list_MonoFL1)
            MonoFL2 = aggregate(my_dict.get("channelPowers")[7].get('power'), list_MonoFL2)
            MonoFL3 = aggregate(my_dict.get("channelPowers")[8].get('power'), list_MonoFL3)
            if KoelcelL1 != None:
                KoelcelTot = KoelcelL1+KoelcelL2+KoelcelL3
                Bordb_wc_Tot = Bordb_wc_L1+Bordb_wc_L2+Bordb_wc_L3
                MonoFTot = MonoFL1+MonoFL2+MonoFL3
                KoelcelTot_CO2 = CO2_omrekenen(elektriciteit, KoelcelTot)
                Bordb_wc_Tot_CO2 = CO2_omrekenen(elektriciteit, Bordb_wc_Tot)
                MonoFtot_CO2 = CO2_omrekenen(elektriciteit, MonoFTot)
                sequence = [
                #Elektriciteit
                "Meter,Smappee2=Verbruik KoelcelL1={}".format(KoelcelL1),
                "Meter,Smappee2=Verbruik KoelcelL2={}".format(KoelcelL2),
                "Meter,Smappee2=Verbruik KoelcelL3={}".format(KoelcelL3),
                "Meter,Smappee2=Verbruik Bordb_wc_L1={}".format(Bordb_wc_L1),
                "Meter,Smappee2=Verbruik Bordb_wc_L2={}".format(Bordb_wc_L2),
                "Meter,Smappee2=Verbruik Bordb_wc_L3={}".format(Bordb_wc_L3),
                "Meter,Smappee2=Verbruik MonoFL1={}".format(MonoFL1),
                "Meter,Smappee2=Verbruik MonoFL2={}".format(MonoFL2),
                "Meter,Smappee2=Verbruik MonoFL3={}".format(MonoFL3),

                #CO2
                "Meter,Smappee2=CO2 KoelcelTot_CO2={}".format(KoelcelTot_CO2),
                "Meter,Smappee2=CO2 Bordb_wc_Tot_CO2={}".format(Bordb_wc_Tot_CO2),
                "Meter,Smappee2=CO2 MonoFtot_CO2={}".format(MonoFtot_CO2)
                ]
                write_api.write(bucket, org, sequence)
            
    client.subscribe(topic)
    client.subscribe(topic2)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
