import time
import random
import math
from animations import animationHelpers

def countdown(pixels, timeInSeconds):
    stepInterval = timeInSeconds / 255
    for i in range(255):
        greenValue = 255 - i
        redValue = i
        pixels.fill((greenValue,redValue, 0))
        pixels.show()
        time.sleep(stepInterval)

def pingPong(pixels, num_pixels, speed, color):
    maxSleepInterval = 0.5

    actualSleepInterval = animationHelpers.getNormalizedSpeed(speed, maxSleepInterval)
    pixels.fill((0,0,0))
    pixels.show()
    for i in range(num_pixels):
        if(i == 0):
            pixels[i] = color
        else:
            pixels[i] = color
            pixels[i-1] = (0,0,0)
        pixels.show()
        time.sleep(actualSleepInterval)
    for i in range(num_pixels-1, -1, -1):
        if(i == num_pixels-1):
            pixels[i] = color
        else:
            pixels[i] = color
            pixels[i+1] = (0,0,0)
        pixels.show()
        time.sleep(actualSleepInterval)

def unifiedRainbow(pixels, speed):
    maxSleepInterval = 0.25

    actualSleepInterval = animationHelpers.getNormalizedSpeed(speed, maxSleepInterval)
    
    for i in range(255):
        scaledColor = animationHelpers.wheel(i)
        pixels.fill(scaledColor)
        pixels.show()
        time.sleep(actualSleepInterval)

def chasingLights(pixels, num_pixels, numLitPixels, color, speed):

    def determineNumberTrailingPixels(currentPixel, numLitPixels):
        if(currentPixel < numLitPixels):
            return currentPixel
        else:
            return numLitPixels

    maxSleepInterval = 0.3
    actualSleepInterval = animationHelpers.getNormalizedSpeed(speed,maxSleepInterval)
    pixels.fill((0,0,0))
    pixels.show()
    for currentPixel in range(num_pixels):
        numTrailingPixels = determineNumberTrailingPixels(currentPixel, numLitPixels)
        for LitPixel in range(numTrailingPixels + 1):
            thePercentage = (numLitPixels - LitPixel) / numLitPixels
            scaledBrightnessValue = animationHelpers.scaleBrightnessOfColor(color, thePercentage)
            pixels[currentPixel-LitPixel] = scaledBrightnessValue
        pixels.show()
        time.sleep(actualSleepInterval)

def twinkle(pixels, num_pixels, speed, color):
    maxSleepInterval = 0.25
    actualSleepInterval = animationHelpers.getNormalizedSpeed(speed, maxSleepInterval)
    def brightnessEquation(brightness, stepSize, iterator):
        return (math.cos(brightness + stepSize*iterator) + 1)*0.5

    brightnessSeeds = [random.random()*2*math.pi for i in range(num_pixels)]
    numberOfSteps = 50
    stepSize = 2.0*math.pi/numberOfSteps
    for i in range(numberOfSteps + 1):
        actualBrightness = [brightnessEquation(brightness, stepSize, i) for brightness in brightnessSeeds]
        for j in range(num_pixels):
            scaledColor = animationHelpers.scaleBrightnessOfColor(color, actualBrightness[j])
            pixels[j] = scaledColor
        pixels.show()
        time.sleep(actualSleepInterval)
    print("COMPLETED ANIMATION")

    #All lights start with some brightness between 0-1 randomly. They will all take a number of steps to go from 
    # 0.5 ->0.6 -> 0.7... 1.0 -> 0.9 -> ...0.1 -> 0.0 ->0.1 ... 0.5
    # Can use a circle to create this looping of values. brightness = (cos(x) +1)*0.5. 
    # x values will be between 0 and 2pi. All pixels will need a starting value that will be iterated on by step size. 
    # step size will be 2pi/numberOfSteps. To progress add one step size to each of the pixels.


def error(pixels):
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(0.5)
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.5)

# Pass in observable to all of the animations
#  1. Start of animation subscribe to observable.
# 2. create value outside of observable
# 3. When the observable fires set the value which was created outside
#4. For most of the animations there is a for loop. At the start of this for loop see if the value has changed. If value has changed then return out of animation. (potentially create blank screen)

