import time
import math
from animations import animationHelpers
# from animations.animationHelpers import *


def scanningStripe(pixels, xAxisLength, speed, color):
    maxSleepInterval = 0.06
    normalizedSpeed = animationHelpers.getNormalizedSpeed(
        speed, maxSleepInterval)

    yAxisLength = int(pixels.n / xAxisLength)
    screen = animationHelpers.createBlankScreen(xAxisLength, yAxisLength)
    for x in range(xAxisLength):
        for y in range(yAxisLength):
            screen[x][y] = color
            screen[xAxisLength-x-1][y] = color
        animationHelpers.show2DimensionalDisplay(pixels, screen)
        screen = animationHelpers.createBlankScreen(xAxisLength, yAxisLength)
        time.sleep(normalizedSpeed)

def circle():
    print('hello')

loopCounter = 0
def movingRainbow(pixels, xAxisLength, speed):
    global loopCounter
    maxColorSpread = 0.5
    normalizedMult = animationHelpers.getNormalizedSpeed(
    speed, maxColorSpread)

    yAxisLength = int(pixels.n / xAxisLength)
    screen = animationHelpers.createBlankScreen(xAxisLength, yAxisLength)
    multiplier = normalizedMult # The bigger the multiplier get the more stripes of rainbow you can see. The smaller, the less distinct. 0.5 max
    for x in range(xAxisLength):
        for y in range(yAxisLength):
            someNumber = (x + loopCounter) * multiplier # + (y + loopCounter) * multiplier
            scaledValue = (math.cos(someNumber) + 1)*255/2.0
            screen[x][y] = animationHelpers.wheel(scaledValue)
    animationHelpers.show2DimensionalDisplay(pixels, screen)
    loopCounter = loopCounter + 1
    # time.sleep(maxSleepInterval)
