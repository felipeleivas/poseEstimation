import random
import cv2




def noisePixels(pixels, noisePercentage):
    height = abs(pixels[0][0] - pixels[2][0])
    width = abs(pixels[0][1] - pixels[1][1])
    heightNoise = height * noisePercentage
    widthNoise = width * noisePercentage
    noisePixels = []
    for pixel in pixels:
        noisePixel = []
        noisedCoordX = random.uniform(-heightNoise, heightNoise) + pixel[0]
        noisedCoordY = random.uniform(-widthNoise, widthNoise) + pixel[1]
        noisePixel.append(noisedCoordX)
        noisePixel.append(noisedCoordY)

        noisePixels.append(noisePixel)
    return noisePixels

