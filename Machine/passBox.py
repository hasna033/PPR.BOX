import RPi.GPIO as GPIO          #RGB LED
import smbus                     #bh1750
from picamera import PiCamera    #Camera
from PIL import Image
from pytesseract import pytesseract
import cv2
import os
import time

DEVICE     = 0x23 

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

CONTINUOUS_LOW_RES_MODE = 0x13
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
ONE_TIME_LOW_RES_MODE = 0x23

bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

red = 13  # Set up Red pin
green = 11  # Set up Green pin
blue = 15  # Set up Blue pin

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # Set GPIO mode to BOARD to use pin numbers

red = 13  # Set up Red pin
green = 11  # Set up Green pin
blue = 15  # Set up Blue pin

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

camera = PiCamera()

# Path to the location of the Tesseract-OCR executable/command
path_to_tesseract = r'/usr/bin/tesseract'

#Point tessaract_cmd to tessaract.exe
pytesseract.tesseract_cmd = path_to_tesseract


def turnOff():
    GPIO.output(red,GPIO.LOW)
    GPIO.output(green,GPIO.LOW)
    GPIO.output(blue,GPIO.LOW)
    
def led():
    GPIO.output(red,GPIO.HIGH)
    GPIO.output(green,GPIO.HIGH)
    GPIO.output(blue,GPIO.HIGH)
    

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  # Read data from I2C interface
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)

if __name__=="__main__":
#     main()

      while True:
#           turnOff()
#           lightLevel=readLight()
#           print("Light Level : " + format(lightLevel,'.1f') + " lx")
#           time.sleep(1)
#           if lightLevel < 10:
#               led()
#               time.sleep(5)
#               camera.rotation = 90
#               camera.start_preview()
#               time.sleep(1)
#               camera.capture('/home/pi/DEProject/images/input8.jpg')
#               camera.stop_preview()
#               turnOff()
#           
              img = Image.open("/home/pi/DEProject/images/input8.jpg")
              text = pytesseract.image_to_string(img)
              
              ## Find the locate of MRZ data
#               print(len(text))       // 439
#               print(text[336:430])
              ##  MRZ location
              MRZ_1 = text[336:386]
              MRZ_2 = text[387:430]
#               print(MRZ_1)
#               print(MRZ_2)
              
              ### separate data mrz 1
              if MRZ_1:
                  ns=""
                  for i in MRZ_1:
                      if(not i.isspace()):
                          ns+=i
#                   print(ns)
                  mrz1 = ns
                  
                  tPass = mrz1[0]        # P, indicating a passport
#                   print("Type : ", tPass)
                  tCode = mrz1[2:5]      # Type for countries
#                   print("Type :" tCode)
                  
                  name = mrz1[5:44]      # Name & Seurname -> ????
#                   print(name)
                  
                  sName = ""
                  fName = ""
                  for i in name:
                      if (i != '<'):
                          sName+=i
                      else:
                          break
                   
#                   print(sName)
#                   print(fName)
              
               ### separate data mrz 2
              if MRZ_2:
                  ns=""
                  for i in MRZ_2:
                      if(not i.isspace()):
                          ns+=i
#                   print(ns)
                  mrz2 = ns
                  print(mrz2)
                  
                  passNum = mrz2[0:9]          # Passport number
                  print("Passport Number: ", passNum)
                  
                  nCode = mrz2[10:13]          # Nationality Code
                  print("Nationality: ", nCode)
                  
                  DOB = mrz2[13:19]           # Date of birth (YYMMDD)
                  print("Date of birth : ", DOB)
                  
                  sex = mrz2[20]           # Sex  (M, F or < for male, female or unspecified)
                  print("Sex : ", sex)
                  
                  EDP = mrz2[21:27]           # Expiration date of passport (YYMMDD)
                  print("Expiration date of passport : ", EDP)
                  
                  persNum = mrz2[28:41]          # Personal number
                  print("Personal number : ", persNum)
                  
                  
                    

              
                  
                  
                  
              
              
              
              
              break





