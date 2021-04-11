# import board
# import neopixel
from animations import twoDAnimations, lightAnimations
from rx import of, subject


# pixels = neopixel.NeoPixel(board.D18, 50, auto_write=False)

shouldIContinueSubject = subject.BehaviorSubject(True)

shouldIContinue = True

def change(shouldIContinue2):
    global shouldIContinue
    shouldIContinue = shouldIContinue2

shouldIContinueSubject.subscribe(change)
for i in range(1000000):
    if(shouldIContinue == False):
        print('Exiting Early: ', i)
        break
    if(i == 8000):
        shouldIContinueSubject.on_next(False)
    something = 7
print("finished for loop")

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