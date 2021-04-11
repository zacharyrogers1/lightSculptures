# import board
# import neopixel
from animations import twoDAnimations, lightAnimations
from rx import of, subject, operators
import time


# pixels = neopixel.NeoPixel(board.D18, 50, auto_write=False)

shouldIContinueSubject = subject.BehaviorSubject(True)

shouldIContinue = True

def change(shouldIContinue2):
    print("Subscriber #1: ", shouldIContinue2)
    time.sleep(5)
    print("Subscriber 1 finished waiting")
    # global shouldIContinue
    shouldIContinue = shouldIContinue2

def change2(idk):
    print("subscriber #2: ", idk)

shouldIContinueSubject.pipe(operators.delay(0.001)).subscribe(change)
shouldIContinueSubject.subscribe(change2)
for i in range(10000000):
    if(shouldIContinue == False):
        print('Exiting Early: ', i)
        break
    if(i == 8000):
        shouldIContinueSubject.on_next(False)
print("finished for loop")

while True:
    something = 7
# # while True:
# #     translate2DPointTo1DPosition(pixels, 4, 3, (30,0,0))
# #     translate2DPointTo1DPosition(pixels, 9, 4, (0,30,0))

# while True:
#     twoDAnimations.scanningStripe(pixels, 10, 5, 0, (155,255,89))


# from rx import of, subject

# hello = of(1,2,3,'hello')
# doot = subject.Subject()


# listener1 = doot.subscribe( lambda value : print("listening to subject: ", value))

# doot.on_next('yo')
# terrible = 'terrible'

# hello.subscribe( lambda value : print(value, terrible))

# Make all of state a behavior subject

# Create a new subject every time a new animation starts so that way you could publish a stop command to the function

# Create a universal way to stop animations