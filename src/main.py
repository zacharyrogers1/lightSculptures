"""CircuitPython Essentials NeoPixel example"""
import time
import board
import neopixel
import deviceState
 
# pixel_pin = board.D18
# num_pixels = 50
 
# ORDER = neopixel.GRB
# pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
#  Green->Red->Blue

deviceState.connectDeviceAndListenForDiff()
 
RED = (0, 255, 0)
GREEN = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)

# Before starting loop connect to AWs and start listening to Diff
# On first connect get the desired state and store it locally.
# Look at the activeAnimation and make the lights start displaying that animation
# deviceState.getActiveAnimationAndRun()

while True:
    deviceState.getActiveAnimationAndRun()
    # time.sleep(1)
    # Every loop go and fetch what animation should be called, then call that animation
    # unifiedRainbow(pixels, 0.2)
    # chasingLights(pixels, num_pixels, 20, WHITE, 0)


# Just start the program from the main.py. Don't need to have the while True grabbing next animation
# Make the device itself automatically fetch the next animation. 
# Have a isAnimationActive behaviorSubject boolean. The device itself will create a permanent subscription. Whenever it is set to false make the subscription get the active animation and restart
# Every animation will need to be listening to the isAnimationActive Subject and when it is false then stop the animation, clear board, return, and unsubscribe.

