import RPi.GPIO as GPIO          #RGB LED
import smbus                     #bh1750
from picamera import PiCamera    #Camera
from PIL import Image
import tesseract
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
    
# def get_string(img_path):
#     # Read image using opencv
#     img = cv2.imread(img_path)
# 
#     # Extract the file name without the file extension
#     file_name = os.path.basename(img_path).split('.')[0]
#     file_name = file_name.split()[0]
# 
#     # Create a directory for outputs
#     output_path = os.path.join(output_dir, file_name)
#     if not os.path.exists(output_path):
#         os.makedirs(output_path)
#         
#         # Rescale the image, if needed.
#         img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
# 
#         # Convert to gray
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 
#         # Apply dilation and erosion to remove some noise
#         kernel = np.ones((1, 1), np.uint8)
#         img = cv2.dilate(img, kernel, iterations=1)
#         img = cv2.erode(img, kernel, iterations=1)
#         # Apply blur to smooth out the edges
#         img = cv2.GaussianBlur(img, (5, 5), 0)
#         
#         # Apply threshold to get image with only b&w (binarization)
#         img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#         
#         # Save the filtered image in the output directory
#         save_path = os.path.join(output_path, file_name + "_filter_" + str(method) + ".jpg")
#         cv2.imwrite(save_path, img)
# 
#         # Recognize text with tesseract for python
#         result = pytesseract.image_to_string(img, lang="eng")
#         return result


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
#           get_string('/home/pi/DEProject/images/input3.jpg')
          print(pytesseract.image_to_string(Image.open('/home/pi/DEProject/images/input3.jpg')))
          
           
          break
          
    
      
          
          
          
            
    

if __name__=="__main__":
   main()




