import RPi.GPIO as GPIO          #RGB LED
import smbus                     #bh1750
from picamera import PiCamera    #Camera
from PIL import Image
import pytesseract
import cv2
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

def turnOff():
    GPIO.output(red,GPIO.LOW)
    GPIO.output(green,GPIO.LOW)
    GPIO.output(blue,GPIO.LOW)
    
def led():
    GPIO.output(red,GPIO.HIGH)
    GPIO.output(green,GPIO.HIGH)
    GPIO.output(blue,GPIO.LOW)
    

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
    

def main():
    
  while True:
      turnOff()
      lightLevel=readLight()
      print("Light Level : " + format(lightLevel,'.1f') + " lx")
      time.sleep(1)
      if lightLevel == 0.0:
          led()
          time.sleep(5)
          camera.rotation = 90
          camera.start_preview()
          time.sleep(1)
          camera.capture('/home/pi/DEProject/images/input3.jpg')
          camera.stop_preview()
          turnOff()
          
#           img = cv2.imread('4.png',cv2.IMREAD_COLOR) #Open the image from which charectors has to be recognized
#           gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey to reduce detials
#           gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
#           original = pytesseract.image_to_string(gray, config='')
#           print (original)
#
           image =Image.open ('./DEProject/images/input3.jpg')
           text = pytesseract.image_to_string(img, config='')
           print (text)
          break
          
    
      
          
          
          
            
    

if __name__=="__main__":
   main()




