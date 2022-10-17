from gpiozero import PwMLED
from time import sleep
import subprocess

bLed = PwMLED(17)
gLed = PwMLED(27)
rLed = PwMLED(22)

