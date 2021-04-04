import time
from animations import animationHelpers

def countdown(pixels, timeInSeconds):
    stepInterval = timeInSeconds / 255
    for i in range(255):
        greenValue = 255 - i
        redValue = i
        pixels.fill((greenValue,redValue, 0))
        pixels.show()
        time.sleep(stepInterval)

def pingPong(pixels, num_pixels, speed, color=(255,0,0)):
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

def unifiedRainbow(pixels, speed, shouldCurrentAnimationStopRunningSubject):
    maxSleepInterval = 0.25

    actualSleepInterval = animationHelpers.getNormalizedSpeed(speed, maxSleepInterval)
    shouldAnimationStop = False

    def setFlagForStop(shouldIStop2):
        nonlocal shouldAnimationStop
        print("Inside subscribe: ", shouldIStop2)
        shouldAnimationStop = shouldIStop2
    
    subscription = shouldCurrentAnimationStopRunningSubject.subscribe(setFlagForStop)
    for i in range(255):
        print("For Loop: ", shouldAnimationStop)
        if (shouldAnimationStop == True):
            pixels.fill((0,0,0))
            pixels.show()
            subscription.dispose()
            return
        pixels.fill(animationHelpers.wheel(i))
        pixels.show()
        time.sleep(actualSleepInterval)
    subscription.dispose()

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

