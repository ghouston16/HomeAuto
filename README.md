# HomeAuto
A Raspberry PI home automation project

### Graphic and Demo Video
Project Outline Graphic: https://github.com/ghouston16/HomeAuto/blob/main/HomeAutoM8Graphic.pdf

Project Demo Video: https://www.youtube.com/playlist?list=PLj34l4tZjW2DP-HuLLLY6FOPE020yqwAI

### Description
* Basic Python Program which gathers environmental data from the house and issues voice commands to google assistant in order to control relevant device state
* Data sent to thingspeak channel where current environmental data is visualised
* Device states also visualised on ThingSpeak Channel
* HTTP server used with cURL commands in order to manually issue command to change device state 

### Dependencies
* Raspbian Os
* Python 3
* Firebase RTB
* Thingspeak
* Google-Text-to-Speach

### Hardware
* Raspberry Pi 3B+
* SenseHat 
* Google Assistant
* Smart Plugs/Devices

### Installation
* Configure RaspberryPi and SenseHat
* Unzip project folder to home directory
* Create ThingSpeak Account/Channel and add API Read/Write Keys to relevant scripts
* Run read_write_process.py in IDE or from command line on PI
