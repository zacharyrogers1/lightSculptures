import time

def translate2DPointTo1DPosition(x, y, xAxisLength):
# The direction the light starts moving first is x direction
    if(y%2 == 0):
        oneDValue = y*xAxisLength + x
    else:
        oneDValue = (y+1)*xAxisLength - (x+1)
    return oneDValue

def createBlankScreen(xAxisLength, yAxisLength):
    noColor = (0,0,0)
    blank2DBoard = [[noColor for i in range(yAxisLength)] for j in range(xAxisLength)]
    return blank2DBoard

def scanningStripe(pixels, xAxisLength, yAxisLength):
    screen = createBlankScreen(xAxisLength, yAxisLength)
    for x in range (xAxisLength):
        for y in range(yAxisLength):
            screen[x][y] = (0,0,255)
        show2DimensionalDisplay(pixels, screen)
        screen = createBlankScreen(xAxisLength, yAxisLength)
        time.sleep(0.5)

def show2DimensionalDisplay(pixels, screen):
    xAxisLength = len(screen)
    yAxisLength = len(screen[0])
    for x in range(xAxisLength):
        for y in range(yAxisLength):
            oneDValue = translate2DPointTo1DPosition(x, y, xAxisLength)
            pixels[oneDValue] = screen[x][y]
    pixels.show()