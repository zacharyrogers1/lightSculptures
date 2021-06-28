import time
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
    for loops in range(200):
        for x in range(xAxisLength):
            for y in range(yAxisLength):
                screen[x][y] = animationHelpers.wheel(x*10 + y*10 + loops)
        animationHelpers.show2DimensionalDisplay(pixels, screen)
        print("screen finish")
    print("-------------------------------")
