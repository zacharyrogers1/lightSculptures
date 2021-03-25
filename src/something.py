"""CircuitPython Essentials NeoPixel example"""
import time
import board
import neopixel
from lightAnimations import *
 
pixel_pin = board.D18
num_pixels = 50
 
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=True, pixel_order=ORDER)
#  Green->Red->Blue
 
 
RED = (0, 255, 0)
GREEN = (255, 0, 0)
BLUE = (0, 0, 255)

 
while True:
    # countdown(pixels, 3)
    # pingPong(pixels, num_pixels, 3, YELLOW)
    chasingLights(pixels, num_pixels, 7, BLUE, 10)