from animations import animationHelpers

def pixelPaint(pixels, xAxisLength, pixelCoordinates):
    for pixelCoordinate in pixelCoordinates:
        pixelIndex = animationHelpers.translate2DPointTo1DPosition(pixelCoordinate["x"], pixelCoordinate["y"], xAxisLength)
        pixels[pixelIndex] = pixelCoordinate["color"]
    pixels.show()
    pixelCoordinates.clear()

