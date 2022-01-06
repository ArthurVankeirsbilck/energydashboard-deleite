# import requests
# import time
# BASE = "http://51.210.255.2:5000/"
# while True:
#     # Verbruik = requests.post(BASE + 'prijs', {"elektriciteitsprijs": 0.24})
#     Get = requests.get(BASE+ 'Data/-7d/now()/Gas/Meter/SmappeeGenW/Algemeen')
#     # print(Verbruik.json())
#     print(Get.json())
#     time.sleep(5)

    
from selenium import webdriver
from time import sleep

driver = webdriver.Firefox()
driver.get('http://51.210.255.2:3000/dashboard/snapshot/2HZhIN9OQ7PdlfBEhq1Ymnzr3g3B9QeE?orgId=1&mode=kiosk&kiosk')
sleep(1)

driver.get_screenshot_as_file("screenshot.png")
driver.quit()
print("end...")