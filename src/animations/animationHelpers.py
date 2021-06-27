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

def scaleBrightnessOfColor(color, percentage):
    return tuple([int(percentage*x) for x in color])


# --------------------------2D--------------------------
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

def show2DimensionalDisplay(pixels, screen):
    xAxisLength = len(screen)
    yAxisLength = len(screen[0])
    for x in range(xAxisLength):
        for y in range(yAxisLength):
            oneDValue = translate2DPointTo1DPosition(x, y, xAxisLength)
            pixels[oneDValue] = screen[x][y]
    pixels.show()