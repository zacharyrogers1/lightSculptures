import board
import neopixel
from animations.lightAnimations import *

pixels = neopixel.NeoPixel(board.D18, 50, auto_write=False)

while True:
    light2Dpixel(pixels, 0, 0, (30,0,0))
