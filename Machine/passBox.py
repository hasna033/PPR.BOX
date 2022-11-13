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

# def read_text_from_image(image):
#   """Reads text from an image file and outputs found text to text file"""
#   # Convert the image to grayscale
#   gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 
#   # Perform OTSU Threshold
#   ret, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
# 
#   rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
# 
#   dilation = cv2.dilate(thresh, rect_kernel, iterations = 1)
# 
#   _, contours, hierachy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#   
#   image_copy = image.copy()
# 
#   result = ""
# 
#   for contour in contours:
#     x, y, w, h = cv2.boundingRect(contour)
# 
#     cropped = image_copy[y : y + h, x : x + w]
# 
#     file = open("results.txt", "r")
# 
#     text = pytesseract.image_to_string(cropped)
#     
#     result += text
#     
# #     print(x, y, w, h, text)
# 
# #     file.write(text)
# #     file.write("\n")
# 
#   file.close()
#   return result
    

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
              print(text)          
                  
              
              
              
              break





