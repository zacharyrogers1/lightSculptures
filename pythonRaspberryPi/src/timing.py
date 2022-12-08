import board
import neopixel
import time
from animations import lightAnimations, twoDAnimations

pixel_pin = board.D18
num_pixels = 100
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
pixels.brightness = 1.0
count = 0.0
start = time.time()
try:
    while(True):
        pixels.fill((255,0,0))
        pixels.show()
        count = count + 1.0
except:
    final = time.time()
    timeElapsed = final-start
    print("Total Time: ", timeElapsed)
    print("Average Time: ", timeElapsed/count)
    print("Additional time per pixel: ",  ((timeElapsed/count) - 5e-5)/num_pixels)