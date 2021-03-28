import time
from animations import animationHelpers
# from animations.animationHelpers import *


def scanningStripe(pixels, xAxisLength, yAxisLength, speed, color):
    maxSleepInterval = 1
    normalizedSpeed = animationHelpers.getNormalizedSpeed(speed, maxSleepInterval)

    screen = animationHelpers.createBlankScreen(xAxisLength, yAxisLength)
    for x in range (xAxisLength):
        for y in range(yAxisLength):
            screen[x][y] = (0,0,255)
        animationHelpers.show2DimensionalDisplay(pixels, screen)
        screen = animationHelpers.createBlankScreen(xAxisLength, yAxisLength)
        time.sleep(normalizedSpeed)
