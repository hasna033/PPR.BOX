import RPi.GPIO as GPIO          #RGB LED
from picamera import PiCamera    #Camera
from PIL import Image
from pytesseract import pytesseract
import os
import time

red = 13            # Set up Red pin
green = 11          # Set up Green pin
blue = 15           # Set up Blue pin
button = 18         # Set up button pin -> input

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)       # Set GPIO mode to BOARD to use pin numbers

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_UP)

camera = PiCamera()

# Path to the location of the Tesseract-OCR executable/command
path_to_tesseract = r'/usr/bin/tesseract'
pytesseract.tesseract_cmd = path_to_tesseract

date_string = time.strftime("%Y-%m-%d-%H:%M")

# # This outputFunction is executed on signal detection
# def outputFunction(null):
#         print("Signal detected")
# 
# # When a signal is detected (falling signal edge) the output function is executed
# GPIO.add_event_detect(button, GPIO.FALLING, callback=outputFunction, bouncetime=100) 
  

def turnOff():
    GPIO.output(red,GPIO.LOW)
    GPIO.output(green,GPIO.LOW)
    GPIO.output(blue,GPIO.LOW)
    
def led():
    GPIO.output(red,GPIO.HIGH)
    GPIO.output(green,GPIO.HIGH)
    GPIO.output(blue,GPIO.HIGH)
    

if __name__=="__main__":
#     main()
      print("Please press the Button to start the process.")
      while True:
          turnOff()
          button_state = GPIO.input(button)
          if button_state == False:
              print("Start the process.")
              led()
              time.sleep(5)
              
              camera.rotation = 90
              camera.start_preview()
              time.sleep(1)
              
              camera.capture(r'/home/pi/DEProject/images/image-' + date_string + '.png')
              camera.stop_preview()
              turnOff()
          
              img = Image.open(r'/home/pi/DEProject/images/image-' + date_string + '.png')
              text = pytesseract.image_to_string(img)
              
              print("Raw:", text)
              break

              
              ## Find the locate of MRZ data
#               print(len(text))       // 439
#               print(text[336:430])
              ##  MRZ location
#           MRZ_1 = text[336:386]
#           MRZ_2 = text[387:430]
#           print("Raw Line 1: ", MRZ_1)
#           print("Raw Line 2:", MRZ_2)
#               
#               ### separate data mrz 1
#               if MRZ_1:
#                   ns=""
#                   for i in MRZ_1:
#                       if(not i.isspace()):
#                           ns+=i
# #                   print(ns)
#                   mrz1 = ns
#                   
#                   firstPart = mrz1.split("<<")[0]
#                   
#                   tPass = firstPart[0]        # P, indicating a passport
# #                   print("Type : ", tPass)
#                   tCode = firstPart[2:5]      # Type for countries
# #                   print("Type :" tCode)
#                   
#                   lastname = firstPart[5:len(firstPart)].replace("<", "-")      # Name & Seurname -> ????
#                   print("Lastname: ",lastname)
#                   
#                   firstname = mrz1.split("<<")[1].replace("<","")
#                   print("Firstname: ",firstname) 
# 
#                ### separate data mrz 2
#               if MRZ_2:
#                   ns=""
#                   for i in MRZ_2:
#                       if(not i.isspace()):
#                           ns+=i
# #                   print(ns)
#                   mrz2 = ns
#                   print(mrz2)
#                   
#                   passNum = mrz2[0:9]          # Passport number
#                   print("Passport Number: ", passNum)
#                   
#                   nCode = mrz2[10:13]          # Nationality Code
#                   print("Nationality: ", nCode)
#                   
#                   DOB = mrz2[13:19]           # Date of birth (YYMMDD)
#                   print("Date of birth : ", DOB)
#                   
#                   sex = mrz2[20]           # Sex  (M, F or < for male, female or unspecified)
#                   print("Sex : ", sex)
#                   
#                   EDP = mrz2[21:27]           # Expiration date of passport (YYMMDD)
#                   print("Expiration date of passport : ", EDP)
#                   
#                   persNum = mrz2[28:41]          # Personal number
#                   print("Personal number : ", persNum)
#                   
#
            



