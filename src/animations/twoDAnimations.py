import time
import math
from animations import animationHelpers


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

def circle(pixels, xAxisLength, color):
    def calculateDist(x, y, centerX, centerY):
        return math.sqrt( abs(centerX-x)**2 + abs(centerY-y)**2)

    yAxisLength = int(pixels.n / xAxisLength)
    centerX = xAxisLength/2
    centerY = yAxisLength/2
    maxDistance = 10
    screen = animationHelpers.createBlankScreen(xAxisLength, yAxisLength)
    for x in range(xAxisLength):
        for y in range(yAxisLength):
            dist = calculateDist(x, y, centerX, centerY)
            scalingPercentage = dist/maxDistance
            if(scalingPercentage>1):
                scalingPercentage = 1
            animationHelpers.scaleBrightnessOfColor(color, scalingPercentage)
            screen[x][y] = color
    pixels.show()

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
