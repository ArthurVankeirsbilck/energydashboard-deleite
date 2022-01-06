from fpdf import FPDF
from paho.mqtt import client as mqtt_client
import random
import json
import requests
import time
import datetime
import locale
import urllib.request
from PIL import Image

def crop_image(naam, l, boven, r, bot):
    im = Image.open(r"Afbeeldingen/{}".format(naam))
 
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    width, height = im.size
    
    # Setting the points for cropped image
    left = l
    top = boven
    right = r
    bottom = bot
    
    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((left, top, right, bottom))
    
    # Shows the image in image viewer
    im1 = im1.save("Afbeeldingen/cropped-{}".format(naam))

def get_graph(time, panelId, ImageName):
    image_url = "http://51.210.255.2:3000/render/d-solo/ZZTOZx5nz/new-dashboard-copy?orgId=1&from=now-{}&to=now&panelId={}&width=1000&height=500&tz=Europe%2FBrussels".format(time, panelId, ImageName)
    urllib.request.urlretrieve(image_url, "Afbeeldingen/{}.png".format(ImageName))
    return ImageName+".png"

def Average(lst):
    return round(sum(lst)/len(lst))

def get_gas(tijd):
    BASE = "http://51.210.255.2:5000/"

    Get = requests.get(BASE+ 'Data/{}/now()/Gas/Meter/SmappeeGenW/Algemeen'.format(tijd))
    list_verbruik = list(Get.json())
    value = sum(list_verbruik)/7.5 
    return round(value, 1), list_verbruik

def get_verbruik(tijd, instal):
    BASE = "http://51.210.255.2:5000/"

    Get = requests.get(BASE+ 'Data/{}/now()/Meter/Smappee1/Verbruik/{}'.format(tijd, instal))
    list_verbruik = list(Get.json())
    value = (sum(list_verbruik)/60)/1000 #Minuut 
    return round(value), list_verbruik

def job():
    if date.today().day != 1:
            dt = datetime.datetime.today()
    locale.setlocale(locale.LC_TIME, 'Dutch')
    tijd = "-30d"

    WIDTH = 210
    HEIGHT = 297
    pdf = FPDF()
    #Pagina 1
    pdf.add_page()
    pdf.image("Afbeeldingen/Red.png", 0, 0, WIDTH, HEIGHT)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0,30, ln=True)
    pdf.cell(0, 40, 'Rapport: {} '.format(dt.strftime("%B")), align="C", ln=True)
    pdf.set_font('Helvetica', '', 14)
    pdf.cell(10)
    pdf.cell(0, 10, txt="1.   Datum ingevuld:", ln=True)
    pdf.cell(10)
    pdf.cell(0, 10, txt="2.   Productiedetails van deze maand:", ln=True)
    crop_image(get_graph("7d", "6", "productie"), 195, 1, 1000, 300)
    pdf.image("Afbeeldingen/{}".format("cropped-"+get_graph("7d", "6", "productie")), 20, 100, 180,66)


    #Pagina 2
    pdf.add_page()
    pdf.image("Afbeeldingen/Red.png", 0, 0, WIDTH, HEIGHT)
    pdf.cell(0,30, ln=True)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 40, 'Verbruiken', align="C", ln=True)
    pdf.set_font('Helvetica', '', 14)
    pdf.cell(10)
    pdf.cell(0, 10, txt="1.   Maand Verbruik: {} kWh".format(get_verbruik(tijd, "NetL1")[0]+get_verbruik(tijd, "NetL2")[0]+get_verbruik(tijd, "NetL3")[0]), ln=True)
    pdf.cell(10)
    pdf.cell(0, 10, txt="2.   Maand PV-Productie : {} kWh".format(get_verbruik(tijd, "SolarL1")[0]+get_verbruik(tijd, "SolarL1")[0]+get_verbruik(tijd, "SolarL1")[0]), ln=True)
    pdf.cell(10)
    pdf.cell(0, 10, txt="3.   Gas verbruik: {} kWh".format(get_gas(tijd)[0]), ln=True)
    pdf.cell(10)
    pdf.cell(0, 10, txt="4.   Gemiddelde Zelfconsumptie: {} %".format(Average(get_verbruik(tijd, "Zc")[1])), ln=True)
    pdf.cell(10)
    pdf.cell(0, 10, txt="5.   Gemiddelde Zelfvoorziening: {} %".format(Average(get_verbruik(tijd, "Zv")[1])), ln=True)


    #Pagina 3
    pdf.add_page()
    pdf.image("Afbeeldingen/Red.png", 0, 0, WIDTH, HEIGHT)
    pdf.cell(0,30, ln=True)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 40, 'Statistieken CO2', align="C", ln=True)
    pdf.image("Afbeeldingen/{}".format(get_graph("7d", "39", "CO21")), 20, 70, 180,90)
    pdf.image("Afbeeldingen/{}".format(get_graph("7d", "43", "CO22")), 10, 170, 180,90)

    #Pagina 4
    pdf.add_page()
    pdf.image("Afbeeldingen/Red.png", 0, 0, WIDTH, HEIGHT)
    pdf.cell(0,30, ln=True)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 40, 'Statistieken elektriciteit', align="C", ln=True)
    # pdf.image("Afbeeldingen/Red.png", 0, 0, WIDTH, HEIGHT)

    pdf.image("Afbeeldingen/{}".format(get_graph("7d", "8", "elek1")), 20, 70, 180,90)
    pdf.image("Afbeeldingen/{}".format(get_graph("7d", "12", "elek2")), 20, 170, 180,90)

    #Pagina 5
    pdf.add_page()
    pdf.image("Afbeeldingen/Red.png", 0, 0, WIDTH, HEIGHT)
    pdf.cell(0,30, ln=True)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 40, 'Statistieken Gas', align="C", ln=True)
    # pdf.image("Afbeeldingen/Red.png", 0, 0, WIDTH, HEIGHT)

    pdf.image("Afbeeldingen/{}".format(get_graph("7d", "37", "gas1")), 20, 70, 180,90)
    pdf.image("Afbeeldingen/{}".format(get_graph("7d", "45", "gas2")), 20, 170, 180,90)

    pdf.output("pdf/rapport-{}.pdf".format(dt.strftime("%B%Y%M")))
    print("Done!")