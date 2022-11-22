import RPi.GPIO as GPIO          #RGB LED
from picamera import PiCamera    #Camera
from PIL import Image, ImageOps, ImageFilter
from pytesseract import pytesseract
import os
import time
import pyrebase

button = 18         # Set up button pin -> input

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)       # Set GPIO mode to BOARD to use pin numbers

GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_UP)

camera = PiCamera()

# Path to the location of the Tesseract-OCR executable/command
path_to_tesseract = r'/usr/bin/tesseract'
pytesseract.tesseract_cmd = path_to_tesseract

date_string = time.strftime("%Y-%m-%d-%H:%M")

config = {
  "apiKey": "AIzaSyA5cw36EoAEwInZAkVbi02QPddJ7WJS30E",
  "authDomain": "passboxdatabase.firebaseapp.com",
  "projectId": "passboxdatabase",
  "databaseURL" : "https://console.firebase.google.com/u/1/project/passboxdatabase/firestore/data/~2FPassportInfo~2F1",
  "storageBucket": "passboxdatabase.appspot.com",
  "messagingSenderId": "118065945023",
  "appId": "1:118065945023:web:55ff3611c97ff76e59690a",
  "measurementId": "G-WZ7M17WFP5"
}


def binarize(img):

  #initialize threshold
  thresh=122

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
#     img = img.crop((550,620,1800,780))
    img = binarize(img)
    img = img.filter(ImageFilter.EDGE_ENHANCE)
    img = img.filter(ImageFilter.SHARPEN)
    img.save(r'/home/pi/DEProject/images/image-' + date_string + '.jpg')
    return img
    
def main():
#       while True:
    print("\nStart the process.\n")
    time.sleep(5)
          
    ## Capture passport picture
    #camera.rotation = 90
    camera.start_preview()
    time.sleep(1)
    
    camera.capture(r'/home/pi/DEProject/images/image-' + date_string + '.jpg')
    camera.stop_preview()
    
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
                
        # persNum = mrz2[28:41]          # Personal number
        # print("Personal number : ", persNum)
        
        print("The process is Done.")
        time.sleep(5)
        
        firebase = pyrebase.initialize_app(config)
        database = firbase.database()
        
        data = {
            "Type ": tPass,
            "Type of Country ": tCode,
            "Firstname ": firstname,
            "Lastname ": lastname,
            "Passport Number ": passNum,
            "Nationality ": nCode,
            "Date of birth ": DOB,
            "Sex ": sex,
            "Expiration date ": EDP
            }
        
                
        for i in range:
            database.child("Passports").child(i).set(data)

                      

if __name__=="__main__":
#     main()
    while True:
        button_state = GPIO.input(button)
        print("Please press the Button to start the process.")
        if button_state == False:
            main()
            break
                  
            




