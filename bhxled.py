import RPi.GPIO as GPIO  #RGB LED
import smbus             #bh1750
import time

# Define some constants from the datasheet
DEVICE     = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

R_PIN = 13  # Set up Red pin
G_PIN = 11  # Set up Green pin
B_PIN = 15  # Set up Blue pin

GPIO.setmode(GPIO.BOARD)  # Set GPIO mode to BOARD to use pin numbers
GPIO.setup(R_PIN, GPIO.OUT)  # Prepare the Red pin to be used
GPIO.setup(G_PIN, GPIO.OUT)  # Prepare the Green pin to be used
GPIO.setup(B_PIN, GPIO.OUT)  # Prepare the Blue pin to be used

string_colors = ['Red', 'Magenta', 'Blue', 'Cyan', 'Green', 'Yellow', 'White']
led_colors = [(1, 0, 0), (1, 0, 1), (0, 0, 1), (0, 1, 1), (0, 1, 0), (1, 1, 0), (1, 1, 1)]

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
    lightLevel=readLight()
    print("Light Level : " + format(lightLevel,'.1f') + " lx")
    time.sleep(0.5)
    if lightLevel == 0:
        for color_tuple in led_colors:  # Iterate over the led_colors array
            # Turn Red, Green & Blue pin on/off based on the color tuple
            GPIO.output([R_PIN, G_PIN, B_PIN], color_tuple)
            index = led_colors.index(color_tuple)  # Get the index to print color name
            print("Color: {}".format(string_colors[index]))  # Print current color name
            time.sleep(3)  # Wait 1.5 seconds
            
    if lightLevel > 0:
        GPIO.cleanup()  # Clear GPIO
    

if __name__=="__main__":
   main()




