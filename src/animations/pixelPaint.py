from animations import animationHelpers

def pixelPaint(pixels, xAxisLength, pixelCoordinates):
    while(len(pixelCoordinates) > 0):
        pixelCoordinate = pixelCoordinates.pop()
        pixelIndex = animationHelpers.translate2DPointTo1DPosition(pixelCoordinate["x"], pixelCoordinate["y"], xAxisLength)
        pixels[pixelIndex] = pixelCoordinate["color"]
    pixels.show()
