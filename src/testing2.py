import board
import neopixel
import time
from animations import lightAnimations, twoDAnimations

pixel_pin = board.D18
num_pixels = 400
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
pixels.brightness = 1.0
redColor = [255,0,0]
while(True):
    lightAnimations.chasingLights(pixels, 20, redColor, 3)