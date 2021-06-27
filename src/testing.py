import board
import neopixel
from animations import lightAnimations

pixel_pin = board.D18
num_pixels = 50
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
pixels.brightness = 0.5
while(True):
    lightAnimations.twinklePreCalc(pixels, num_pixels, 1.0, (255,0,0))
    # pixels[0:3] = [(255,0,0),(255,0,0),(255,0,0)]
    # pixels.show()


# import random

# numberOfSteps = 20
# num_pixels = 50
# brightnessLookup = [float(x)/numberOfSteps for x in range(numberOfSteps)]
# startingPoints = [random.randint(0, numberOfSteps-1) for x in range(num_pixels)]
# for i in range(numberOfSteps):
#     newSpot = startingPoints[0]+i
#     if(newSpot >= numberOfSteps):
#         newSpot = newSpot - numberOfSteps
#     brightness = brightnessLookup[newSpot]
#     print(brightness)