from animations import animationHelpers

def pixelPaint(pixels, xAxisLength, pixelCoordinate):
    pixelIndex = animationHelpers.translate2DPointTo1DPosition(pixelCoordinate["x"], pixelCoordinate["y"], xAxisLength)
    pixels[pixelIndex] = pixelCoordinate["color"]
    pixels.show()

