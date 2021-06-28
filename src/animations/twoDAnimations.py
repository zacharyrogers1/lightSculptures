import time
import math
from animations import animationHelpers
# from animations.animationHelpers import *


def scanningStripe(pixels, xAxisLength, speed, color):
    maxSleepInterval = 0.2
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


def movingRainbow(pixels, xAxisLength, speed):
    yAxisLength = int(pixels.n / xAxisLength)
    screen = animationHelpers.createBlankScreen(xAxisLength, yAxisLength)
    loopCount = 8000
    # maxValue = xAxisLength + loopCount
    # scalingFactor = (2*math.pi)/maxValue
    for loops in range(loopCount):
        for x in range(xAxisLength):
            for y in range(yAxisLength):
                someNumber = (x + loops) * 0.2
                scaledValue = (math.cos(someNumber) + 1)*255/2.0
                screen[x][y] = animationHelpers.wheel(scaledValue)
            animationHelpers.show2DimensionalDisplay(pixels, screen)
