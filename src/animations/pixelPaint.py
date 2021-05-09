from animations import animationHelpers

def pixelPaint(pixels, xAxisLength, pixelCoordinates, brightness):
    while(len(pixelCoordinates) > 0):
        pixelCoordinate = pixelCoordinates.pop()
        pixelIndex = animationHelpers.translate2DPointTo1DPosition(pixelCoordinate["x"], pixelCoordinate["y"], xAxisLength)
        scaledColor = animationHelpers.scaleBrightnessOfColor(pixelCoordinate["color"], brightness)
        pixels[pixelIndex] = scaledColor
    pixels.show()
