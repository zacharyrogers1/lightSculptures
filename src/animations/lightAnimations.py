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

def pingPong(pixels, speed, color):
    maxSleepInterval = 0.02

    actualSleepInterval = animationHelpers.getNormalizedSpeed(speed, maxSleepInterval)
    pixels.fill((0,0,0))
    pixels.show()
    num_pixels = pixels.n
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
    maxSleepInterval = 0.05

    actualSleepInterval = animationHelpers.getNormalizedSpeed(speed, maxSleepInterval)
    
    for i in range(255):
        scaledColor = animationHelpers.wheel(i)
        pixels.fill(scaledColor)
        pixels.show()
        time.sleep(actualSleepInterval)

def chasingLights(pixels, numLitPixels, color, speed):
    def getWrapAroundNumber(index, positionsBehindIndex, arraySize):
        positionToIndex = index-positionsBehindIndex
        if(positionToIndex < 0 ):
            return positionToIndex+arraySize
        elif(positionToIndex>=arraySize):
            return positionToIndex - arraySize
        else:
            return positionToIndex

    num_pixels = pixels.n
    brightSpotPositions = [25, 325]
    for animationStepNum in range(num_pixels):
        for j in range(len(brightSpotPositions)):
            brightSpotPosition = brightSpotPositions[j]
            for i in range(numLitPixels+1):
                brightness = (numLitPixels - i)/numLitPixels
                position = getWrapAroundNumber(brightSpotPosition, i, num_pixels)
                scaledBrigtnessValue = animationHelpers.scaleBrightnessOfColor(color, brightness)
                pixels[position] = scaledBrigtnessValue
            brightSpotPositions[j] = brightSpotPositions[j] + 1
        pixels.show()

brightnessSeeds = None
def twinkle(pixels, speed, color):
    global brightnessSeeds
    minimumSteps = 5
    maximumSteps = 200
    num_pixels = pixels.n
    def brightnessEquation(brightness, stepSize, iterator):
        return (math.cos(brightness + stepSize*iterator) + 1)*0.5
    if(brightnessSeeds == None):
        brightnessSeeds = [random.random()*2*math.pi for i in range(num_pixels)]

    numberOfSteps = minimumSteps + int((maximumSteps-minimumSteps)*speed)
    stepSize = 2.0*math.pi/numberOfSteps
    for i in range(numberOfSteps):
        actualBrightness = [brightnessEquation(brightness, stepSize, i) for brightness in brightnessSeeds]
        pixelsTuple = [animationHelpers.scaleBrightnessOfColor(color, x) for x in actualBrightness]
        pixels[:num_pixels] = pixelsTuple
        pixels.show()
    #All lights start with some brightness between 0-1 randomly. They will all take a number of steps to go from 
    # 0.5 ->0.6 -> 0.7... 1.0 -> 0.9 -> ...0.1 -> 0.0 ->0.1 ... 0.5
    # Can use a circle to create this looping of values. brightness = (cos(x) +1)*0.5. 
    # x values will be between 0 and 2pi. All pixels will need a starting value that will be iterated on by step size. 
    # step size will be 2pi/numberOfSteps. To progress add one step size to each of the pixels.

def off(pixels):
    pixels.fill((0,0,0))
    pixels.show()

def fillAndEmpty(pixels, speed, color):
    maxSleepInterval = 0.015
    actualSleepInterval = animationHelpers.getNormalizedSpeed(speed, maxSleepInterval)
    off(pixels)
    for i in range(pixels.n):
        pixels[i] = color
        pixels.show()
        time.sleep(actualSleepInterval)
    for i in range(pixels.n):
        pixels[pixels.n-i-1] = (0,0,0)
        pixels.show()
        time.sleep(actualSleepInterval)

def static(pixels, color):
    pixels.fill(color)
    pixels.show()
    time.sleep(0.1)

def error(pixels):
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(0.5)
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.5)

