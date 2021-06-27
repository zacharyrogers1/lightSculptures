import board
import neopixel
from animations import lightAnimations

pixel_pin = board.D18
num_pixels = 3
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
pixels.brightness = 0.5
while(True):
    # lightAnimations.twinkle(pixels, num_pixels, 0.0, (255,0,0))
    pixels[0:3] = [(255,0,0),(255,0,0),(255,0,0)]
    pixels.show()

# someList = [9,22,32]
# someList[:3] = [5,5,5]
# print(someList)
