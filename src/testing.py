import board
import neopixel       
       
pixel_pin = board.D18
num_pixels = 50
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
pixels.brightness = 0.1
while(True):
    pixels.fill((255,0,0))
    pixels.show()