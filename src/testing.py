# import board
# import neopixel
from animations import twoDAnimations, lightAnimations
from rx import of, subject, operators, interval
from rx.scheduler import ThreadPoolScheduler
from threading import current_thread
import time
import multiprocessing
import random

def functionWhichPopsOff(aList):
    while (len(aList) > 0):
        someValue = aList.pop()
        print("single value: ", someValue)


someList = [1,2,3,4,5,6]

functionWhichPopsOff(someList)

print(someList)



