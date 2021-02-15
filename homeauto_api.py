#!/usr/bin/python3

import os
from flask import Flask, request
from flask_cors import CORS
from sense_hat import SenseHat
import text_speech
import json
import time
import datetime
import urllib3
import requests
from urllib.request import urlopen
import requests
import logging

# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing is the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig(filename='homeAutoM8.log', level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

dt_now = datetime.datetime.now()
t_now = dt_now.time()
now = dt_now.time().strftime("%H:%M:%S")
wake = 'Hey Google ! '

heatStatus = []
humStatus = []
sense = SenseHat()
READ_API_KEY=<YOU_API_KEY>

#clear sensehat
sense.clear()

app = Flask(__name__)
CORS(app)

#
# use thing_read.py to get values instead of sensors ##
#
# Most recent Humidifier and Heating Status Read from json
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
print('Humidifier:' + hum_status)
print('Heating:' + heat_status)
print()

# Returns Temp on http GET
@app.route('/sensehat/temp',methods=['GET'])
def current_temp():
    temp=round(sense.get_temperature(),2)
    return str(temp)

# Returns Hum on http GET
@app.route('/sensehat/hum',methods=['GET'])
def current_hum():
    temp=round(sense.get_humidity(),2)
    return str(hum)
# Returns Pressure on http GET
@app.route('/sensehat/press',methods=['GET'])
def current_press():
    temp=round(sense.get_pressure(),2)
    return str(press)
# Returns heating Status
@app.route('/sensehat/heating',methods=['GET'])
def heating_get():
    #check status string
    if heat_status == "Off":
        return '{"state":"off"}'
    else:
            return '{"state":"on"}'
# Returns Humidifier Status
@app.route('/sensehat/hum',methods=['GET'])
def humidifier_get():
    #check status string
    if heat_status == "Off":
        return '{"state":"off"}'
    else:
            return '{"state":"on"}'
# Changes Heat Status on HTTP POST
@app.route('/sensehat/heating',methods=['POST'])
def heat_post():
    print()
    print('Heating')
    state=request.args.get('state')
    print (state)
    if (state=="on"):
        heat_status = "On"
       # text_speech.myCommand(wake)
        mytext = 'Turn the Heat On'
        text_speech.myCommand(mytext)
        os.system('python3 smtp_heatOn.py')
        print()
        print('Heating:')
        return '{"state":"on"}'
        print()
    else:
        heat_status = "Off"
        mytext = 'Turn the Heat Off'
       # text_speech.myCommand(wake)
        text_speech.myCommand(mytext)
        os.system('python3 smtp_heatOff.py')
        print()
        print('Heating: ')
        return '{"state":"off"}'
        print()

# Changes Heat Status on HTTP POST
@app.route('/sensehat/hum',methods=['POST'])
def hum_post():
    print()
    print('Humidifier:')
    state=request.args.get('state')
    print (state)
    if (state=="on"):
        hum_status = "On"
       # text_speech.myCommand(wake)
        mytext = 'Turn the Humidity On'
        text_speech.myCommand(mytext)
        os.system('python3 smtp_humOn.py')
        print()
        print('Humidifier')
        return '{"state":"on"}'
        print()
    else:
        hum_status = "Off"
        mytext = 'Turn the Humidity Off'
        #text_speech.myCommand(wake)
        text_speech.myCommand(mytext)
        os.system('python3 smtp_heatOn.py')
        print()
        print('Humidifier')
        return '{"state":"on"}'
        print()
        return '{"state":"off"}'
    print()
# Runs server on Port 5000
if __name__ == "__main__":
    #Run API on port 5000, set debug to true
    app.run(host='0.0.0.0', port=5000, debug=True)
