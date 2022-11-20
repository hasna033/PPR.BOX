from picamera import PiCamera
import time

camera = PiCamera()
camera.start_preview()
time.sleep(1)
    
camera.capture(r'/home/pi/DEProject/images/calibrate.jpg')
camera.stop_preview()