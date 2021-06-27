import board
import neopixel
from animations import lightAnimations

pixel_pin = board.D18
num_pixels = 50
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
pixels.brightness = 0.5
while(True):
    lightAnimations.twinkle(pixels, num_pixels, 0, (255,0,0))


# import math
# import random
# pixelCount = 20
# startingBrightnessValues = [
#     random.random()*2*math.pi for i in range(pixelCount)]
# numberOfSteps = 10
# stepSize = 2.0*math.pi/numberOfSteps

# # print(startingBrightnessValues)

# def brightnessEquation(brightness, stepSize, iterator):
#     return (math.cos(brightness + stepSize*iterator) + 1)*0.5

# for i in range(numberOfSteps+1):
#     actualBrightness = [brightnessEquation(brightness, stepSize, i) for brightness in startingBrightnessValues]
#     # startingBrightnessValues = [x + stepSize for x in startingBrightnessValues]
#     print(actualBrightness)
