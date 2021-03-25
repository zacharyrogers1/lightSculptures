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
 
 
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
 
while True:
    # countdown(pixels, 3)
    # pingPong(pixels, num_pixels, 3, YELLOW)
    unifiedRainbow(pixels, 3)