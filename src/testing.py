import board
import neopixel
from animations.lightAnimations import *

pixels = neopixel.NeoPixel(board.D18, 50, auto_write=False)

# while True:
#     translate2DPointTo1DPosition(pixels, 4, 3, (30,0,0))
#     translate2DPointTo1DPosition(pixels, 9, 4, (0,30,0))


createStripe(pixels, 10, 5)
print(str(pixels))