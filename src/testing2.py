import board
import neopixel
import time
from animations import lightAnimations, twoDAnimations

pixel_pin = board.D18
num_pixels = 400
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
pixels.brightness = 0.3
pixels.fill((0,255,0))
pixels.show()
while(True):
    time.sleep(1)