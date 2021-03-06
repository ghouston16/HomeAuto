#!/usr/bin/python3

import pyrebase 

import requests 
from urllib.request import urlopen  
import urllib3 
urllib3.disable_warnings()  
import json 
import time 
from sense_hat import SenseHat 
import os 
import text_speech 
import smtplib, ssl
# ThingSpeak Read Key
READ_API_KEY='YOUR_API_KEY' 
CHANNEL_ID= <YOUR_CHANNEL_ID>

# import hum_control
import datetime
sense = SenseHat()
humStatus = []
heatStatus = []
# ThingSpeak Write Key
WRITE_API_KEY='YOUR_WRITE_API_KEY'

baseURL='https://api.thingspeak.com/update?api_key=WRITE_API_KEY'

# Firebase Config
config = {
  "apiKey": "api_key",
  "authDomain": "YOUR_AUTH_DOMAIN",
  'storageBucket': 'YOUR_STORAGE_BUCKET,
  'databaseURL':'YOUR_DB_URL'
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
wake='  Hey Google  '
# Url for heat off POST Request
# heatingOff = "http://192.168.137.159:5000/sensehat/light?state=off"
# heatingOn = "http://192.168.137.159:5000/sensehat/light?state=on"

# Most recent Humidifier and Heating Status Read from json
with open('climateData.json') as json_file:
  data = json.load(json_file)
  hum_start = data['Humidifier']
  humStatus.insert(0, hum_start)
  heat_start = data['Heating']
  heatStatus.insert(0, hum_start)

hum_status = heatStatus[0]
#hum_status = thing_read.hum_status()
heat_status = heatStatus[0]
print()
print("Sending Home Climate Data ThingSpeak & FB Using Pi")
print("--------------------------------------------------")
t = time.localtime()
sense.clear()



def writeData(temp,hum,press,thingHeat,thingHum):
    # Sending the data to thingspeak in the query string
    conn = urlopen(baseURL + '&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s' % (temp,hum,press,thingHeat,thingHum))
    print(conn.read())
    # Closing the connection
    conn.close

while True:
    dt_now = datetime.datetime.now()
    t_now = dt_now.time()
    now = dt_now.time().strftime("%H:%M:%S")
    # Setting intial decision window for device
    # State changes
    t_heatOn = datetime.time(hour=0, minute=00)
    t_heatOff = datetime.time(hour=16, minute=00)
    # Get sensor Data from SenseHat
    temp=round(sense.get_temperature(),2)
    press=round(sense.get_pressure(),2)
    hum=round(sense.get_humidity(),2)
    # Checks current time against set heat on/off times
    # Checks temp and then heating status
    # Decides action updates status as needed
    if t_now > t_heatOn and t_now < t_heatOff:
      if temp <= 35 and heatStatus[0] == "Off":
        mytext = 'Turn the Heat On'
      # requests.post(heatingOn) -- This method call works but ties
      # script to server function s
       # text_speech.myCommand(wake)
        text_speech.myCommand(mytext)
        os.system('python3 smtp_heatOn.py') # Email Notification
        print()
        heatStatus.insert(0, "On")
        print('Heating Status:')
        print(heatStatus[0])
        print()
      # Temp Over 40 turn OFF
      elif temp > 38 and heatStatus[0] == "On":
        #requests.post(heatingOff)
        #text_speech.myCommand(wake)
        mytext = 'Turn the Heat Off'
        text_speech.myCommand(mytext)
        print()
        os.system('python3 smtp_heatOff.py')
        heatStatus.insert(0, "Off")
        print('Heating Status:')
        print(heatStatus[0])
        print()
      if hum < 35 and humStatus[0] == "Off":
        mytext = 'Turn the Humidity On'
       # text_speech.myCommand(wake)
        text_speech.myCommand(mytext)
        humStatus.insert(0, "On")
        hum_status = humStatus[0]
        os.system('python3 smtp_humOn.py')
        print('Humidifier: ' + hum_status)
        print()
      elif hum >= 45 and humStatus[0] == "On":
        #text_speech.myCommand(wake)
        mytext = 'Turn the Humidity Off'
        os.system('python3 smtp_humOff.py')
        text_speech.myCommand(mytext)
        humStatus.insert(0, "Off")
        print('Humidifier: ' + hum_status)
        print()
    elif (t_now < t_heatOn or t_now > t_heatOff) and heatStatus[0] == "On":
      mytext = 'Turn the Heat Off'
      #text_speech.myCommand(wake)
      text_speech.myCommand(mytext)
      os.system('python3 smtp_heatOff.py')
      print()
      heatStatus.insert(0, "Off")
      print('Heating Status:')
      print(heatStatus[0])
      print()
    if (t_now < t_heatOn or t_now > t_heatOff) and (humStatus[0] == "On"):
      mytext = 'Turn the Humidity Off'
     # text_speech.myCommand(wake)
      text_speech.myCommand(mytext)
      humStatus.insert(0, 'Off')
      os.system('python3 smtp_humOff.py')
      print('Humidifier: ' + hum_status)
      print()

    # Climate Data JSON object
    data = {
      "Temp": temp,
      "Humidity": hum,
      "Pressure": press,
      "Heating": heatStatus[0],
      "Humidifier": humStatus[0],
      "Timestamp": dt_now.strftime("%H:%M:%S %d/%m/%Y")
    }
    # Convert Heating and Hum Status to 1/0 from ThingSpeak
    if heatStatus[0] == "On":
      thingHeat = 1
    else:
      thingHeat = 0
    if humStatus[0] == "On":
      thingHum = 1
    else:
      thingHum = 0

    # Data sent to ThingSpeak + printed in JSON
    writeData(temp,hum,press,thingHeat,thingHum)
    print(data)
    print()
    # Writes most recent data to json file
    with open('climateData.json', 'w') as json_file:
      json.dump(data, json_file)  # json_file

    # Data sent to Firebase -- opted aginst FB for other functions
    # Left in for fututure dev
    # Most recent data overwrites 'set' branch of db
    db.child("sense").child("1-set").set(data)
    # Data pushed to main branch of db
    db.child("sense").child("2-push").push(data)
    time.sleep(15)
