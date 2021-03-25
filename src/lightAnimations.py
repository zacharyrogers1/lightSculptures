import time

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

    actualSleepInterval = getNormalizedSpeed(speed, maxSleepInterval)
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

def getNormalizedSpeed(speed, maxSleepInterval):
    if(speed > 1.0):
        return 1.0 * maxSleepInterval
    elif(speed < 0):
        return 0 
    return speed * maxSleepInterval


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def unifiedRainbow(pixels, speed):
    maxSleepInterval = 0.25

    actualSleepInterval = getNormalizedSpeed(speed, maxSleepInterval)
    for i in range(255):
        pixels.fill(wheel(i))
        pixels.show()
        time.sleep(actualSleepInterval)

def scaleBrightnessOfColor(color, percentage):
    return tuple([percentage*x for x in color])

def chasingLights(pixels, num_pixels, numLitPixels, color, speed):

    def determineNumberTrailingPixels(currentPixel, numLitPixels):
        if(currentPixel < numLitPixels):
            return currentPixel
        else:
            return numLitPixels

    
    maxSleepInterval = 0.3
    actualSleepInterval = getNormalizedSpeed(speed,maxSleepInterval)
    pixels.fill((0,0,0))
    pixels.show()
    for currentPixel in range(num_pixels):
        numTrailingPixels = determineNumberTrailingPixels(currentPixel, numLitPixels)
        for LitPixel in range(numTrailingPixels + 1):
            thePercentage = (numLitPixels - LitPixel) / numLitPixels
            scaledBrightnessValue = scaleBrightnessOfColor(color, thePercentage)
            pixels[currentPixel-LitPixel] = scaledBrightnessValue
        pixels.show()
        time.sleep(actualSleepInterval)