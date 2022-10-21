from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (1366, 768)
camera.rotation = 90

camera.start_preview()
sleep(3)
camera.capture('/home/pi/Desktop/image2.jpg')
camera.stop_preview()