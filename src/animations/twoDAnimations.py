import time
from animationHelpers import *


def scanningStripe(pixels, xAxisLength, yAxisLength, speed, color):
    maxSleepInterval = 1
    normalizedSpeed = getNormalizedSpeed(speed, maxSleepInterval)

    screen = createBlankScreen(xAxisLength, yAxisLength)
    for x in range (xAxisLength):
        for y in range(yAxisLength):
            screen[x][y] = (0,0,255)
        show2DimensionalDisplay(pixels, screen)
        screen = createBlankScreen(xAxisLength, yAxisLength)
        time.sleep(normalizedSpeed)
