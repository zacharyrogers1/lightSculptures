import board
import neopixel
import time
from animations import lightAnimations, twoDAnimations

pixel_pin = board.D18
num_pixels = 100
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
pixels.brightness = 1.0
average = 0
flip = True
try:
    while(True):
        start = time.time()
        if(flip):
            pixels.fill((255,0,0))
            pixels.show()
        else:
            pixels.fill((0,255,0))
            pixels.show()
        final = time.time()
        timeElapsed = final-start
        average = (average + timeElapsed)/2.0
        flip = not flip
except:
    print("Average Time: ", average)
    print("Number Of Pixels: ", num_pixels)