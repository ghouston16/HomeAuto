#!/usr/bin/env python
from urllib.request import urlopen
import json
import time
READ_API_KEY='BD51E7YUF68EK8S5'
CHANNEL_ID= 1225740


def main():
    conn = urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                           % (CHANNEL_ID,READ_API_KEY))
    response = conn.read()
    data=json.loads(response)
    temp=data['field1']
    hum=data['field2']
    press=data['field3']
    thingHeat=data['field4']
    if thingHeat == "0":
      heat_status = "Off"
    else:
      heat_status = "On"
    thingHum=data['field5']
    if thingHum == "0":
      hum_status = "Off"
    else:
      hum_status = "On" 
    print("Temperature: " + temp + ' C')
    print("Humidity: " + hum + '%')
    print("Pressure: " + press + ' millibars')
    print("Heating: " + heat_status)
    print("Humidifier: " + hum_status)
    print()
    conn.close()

def hum_status():
    conn = urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                           % (CHANNEL_ID,READ_API_KEY))
    response = conn.read()
    data=json.loads(response)
    thingHum=data['field5']
    if thingHum == "0":
      hum_status = "Off"
    else:
      hum_status = "On" 
    return hum_status
    conn.close()

while True:
   main()
   time.sleep(30)
