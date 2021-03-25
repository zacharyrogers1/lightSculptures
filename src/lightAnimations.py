import time

def countdown(pixels, timeInSeconds):
    stepInterval = timeInSeconds / 255
    for i in range(255):
        greenValue = 255 - i
        redValue = i
        pixels.fill((greenValue,redValue, 0))
        time.sleep(stepInterval)

def pingPong(pixels, num_pixels, timeInSeconds, color=(255,0,0)):
    stepInterval = timeInSeconds / (num_pixels * 2)
    pixels.fill((0,0,0))
    for i in range(num_pixels):
        if(i == 0):
            pixels[i] = color
        else:
            pixels[i] = color
            pixels[i-1] = (0,0,0)
        time.sleep(stepInterval)
    for i in range(num_pixels-1, -1, -1):
        if(i == num_pixels):
            pixels[i] = color
        else:
            pixels[i] = color
            pixels[i+1] = (0,0,0)
        time.sleep(stepInterval)