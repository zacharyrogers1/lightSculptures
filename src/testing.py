# import board
# import neopixel
# from animations import twoDAnimations

# pixels = neopixel.NeoPixel(board.D18, 50, auto_write=False)

# # while True:
# #     translate2DPointTo1DPosition(pixels, 4, 3, (30,0,0))
# #     translate2DPointTo1DPosition(pixels, 9, 4, (0,30,0))

# while True:
#     twoDAnimations.scanningStripe(pixels, 10, 5, 0, (155,255,89))


from rx import of, subject

hello = of(1,2,3,'hello')
doot = subject.Subject()


listener1 = doot.subscribe( lambda value : print("listening to subject: ", value))

doot.on_next('yo')
terrible = 'terrible'

hello.subscribe( lambda value : print(value, terrible))

# Make all of state a behavior subject

# Create a new subject every time a new animation starts so that way you could publish a stop command to the function

# Create a universal way to stop animations