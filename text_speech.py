# Import the required module for text to speech conversion
from gtts import gTTS
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os 
import time
from sense_hat import SenseHat

sense = SenseHat()

temp=round(sense.get_temperature(),2)

def myCommand(mytext):
  # Language in which you want to convert  
  language = 'en'
# Passing the text and language to the engine
  myobj = gTTS(text=mytext, lang=language, slow=False) 
  
# Saving the converted audio in a mp3 file named 
# cimate_ctrl 
  myobj.save("climate_ctrl.mp3") 
  
# Playing the converted file
  os.system("mpg321 wake.mp3") 
  os.system("mpg321 climate_ctrl.mp3") 
