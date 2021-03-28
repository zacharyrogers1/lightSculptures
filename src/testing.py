import board
import neopixel
from animations import twoDAnimations

pixels = neopixel.NeoPixel(board.D18, 50, auto_write=False)

# while True:
#     translate2DPointTo1DPosition(pixels, 4, 3, (30,0,0))
#     translate2DPointTo1DPosition(pixels, 9, 4, (0,30,0))

while True:
    twoDAnimations.scanningStripe(pixels, 10, 5, 0, (155,255,89))