import RPi.GPIO as GPIO          #RGB LED
from picamera import PiCamera    #Camera
from PIL import Image, ImageOps, ImageFilter
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

def turnOff():
    GPIO.output(red,GPIO.LOW)
    GPIO.output(green,GPIO.LOW)
    GPIO.output(blue,GPIO.LOW)
    
def led():
    GPIO.output(red,GPIO.HIGH)
    GPIO.output(green,GPIO.HIGH)
    GPIO.output(blue,GPIO.HIGH)

def binarize(img):

  #initialize threshold
  thresh=95

  #convert image to greyscale
  img=img.convert('L') 

  width,height=img.size

  #traverse through pixels 
  for x in range(width):
    for y in range(height):

      #if intensity less than threshold, assign white
      if img.getpixel((x,y)) < thresh:
        img.putpixel((x,y),0)

      #if intensity greater than threshold, assign black 
      else:
        img.putpixel((x,y),255)

  return img

def preprocess(img):
    img2 = img.crop((550,620,1800,780))
    img2 = binarize(img2)
    img2 = img2.filter(ImageFilter.EDGE_ENHANCE)
    img2 = img2.filter(ImageFilter.SHARPEN)
    img2.save(r'/home/pi/DEProject/images/prepocessed.jpg')
    return img2
    
def main():
#       while True:
    print("\nStart the process.\n")
    #led()
    time.sleep(5)
          
    ## Capture passport picture
    #camera.rotation = 90
    camera.start_preview()
    time.sleep(1)
    
    camera.capture(r'/home/pi/DEProject/images/image-' + date_string + '.jpg')
    camera.stop_preview()
    turnOff()
    
    img = Image.open(r'/home/pi/DEProject/images/image-' + date_string + '.jpg')
    # Preprocess image
    img = preprocess(img)
    text = pytesseract.image_to_string(img, lang='eng')
    print(text)
    
    ## Find the locate of MRZ location
    MRZ_1 = text.splitlines()[0]
    MRZ_2 = text.splitlines()[1]
    #            print("Raw Line 1: ", MRZ_1)
    #            print("Raw Line 2: ", MRZ_2)
    print("Passport's Information\n")
          
    ## separate data mrz 1
    if MRZ_1:
        ns=""
        for i in MRZ_1:
            if(not i.isspace()):
                ns+=i
                #  print(ns)
            mrz1 = ns
        firstPart = mrz1.split("<<")[0]
        
        tPass = firstPart[0:1]        # P, indicating a passport
        print("Type : ", tPass)
        tCode = firstPart[2:5]      # Type for countries
        print("Type for Countries: ", tCode)
                
        lastname = firstPart[5:len(firstPart)].replace("<", "-")      # Name & Seurname -> ????
        print("Lastname: ",lastname)
                
        firstname = mrz1.split("<<")[1].replace("<","")
        print("Firstname: ",firstname)
          
    ## separate data mrz 2
    if MRZ_2:
        ns=""
        for i in MRZ_2:
            if(not i.isspace()):
                ns+=i
                #   print(ns)
            mrz2 = ns
        # print(mrz2)
        # print(len(mrz2))
                
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
        
        print("The process is Done.")
                      

if __name__=="__main__":
    main()
#     while True:
#         button_state = GPIO.input(button)
#         turnOff()
#         print("Please press the Button to start the process.")
#         if button_state == False:
#             main()
                  
                  
            




