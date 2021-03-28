"""CircuitPython Essentials NeoPixel example"""
import time
import board
import neopixel
from animations.lightAnimations import *
from deviceState import *
 
# pixel_pin = board.D18
# num_pixels = 50
 
# ORDER = neopixel.GRB
# pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
#  Green->Red->Blue

connectDeviceAndListenForDiff()
 
RED = (0, 255, 0)
GREEN = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)

# Before starting loop connect to AWs and start listening to Diff
# On first connect get the desired state and store it locally.
# Look at the activeAnimation and make the lights start displaying that animation
 
while True:
    time.sleep(1)
    # Every loop go and fetch what animation should be called, then call that animation
    # unifiedRainbow(pixels, 0.2)
    # chasingLights(pixels, num_pixels, 20, WHITE, 0)

