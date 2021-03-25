"""CircuitPython Essentials NeoPixel example"""
import time
import board
import neopixel
from lightAnimations import *
 
pixel_pin = board.D18
num_pixels = 50
 
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
#  Green->Red->Blue
 
RED = (0, 255, 0)
GREEN = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)

 
while True:
    # countdown(pixels, 3)
    # pingPong(pixels, num_pixels, 0, RED)
    # pingPong(pixels, num_pixels, 0.5, RED)
    # pingPong(pixels, num_pixels, 0.25, RED)
    # unifiedRainbow(pixels, 0)
    # unifiedRainbow(pixels, 0.33)
    chasingLights(pixels, num_pixels, 20, WHITE, 0)
    chasingLights(pixels, num_pixels, 20, BLUE, 0.1)
    chasingLights(pixels, num_pixels, 20, GREEN, 1.0)
    # unifiedRainbow(pixels, 3)