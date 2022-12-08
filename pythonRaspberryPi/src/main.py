"""CircuitPython Essentials NeoPixel example"""
import time
import board
import neopixel
import deviceState

deviceState.connectDeviceAndListenForDiff()

while True:
    deviceState.getActiveAnimationAndRun()
