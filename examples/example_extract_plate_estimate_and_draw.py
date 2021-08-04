import cv2

import plate_detectation.example_plate_detection as plate_detection
from calibration import getMatrix
from camera import K, getPixelPointFromRealWorldCordinates
from util import *


coordinates = [[0, 0, 0], [0.4, 0, 0], [0.4, .13, 0], [0, .13, 0]]
if __name__ == '__main__':
    imagePath = 'videos/hb20_30_cutted_output.mp4'
    image = cv2.imread(imagePath)
    pixels = plate_detection.getLPPoints(imagePath)
    # pixels = [[658,325],[1040,320],[1045,435],[658,439]]
    print('\n\n\n\n\n')

    print('Extracted points:')
    for pixel in pixels:
        print(pixel)

    # coordinates = [[0, 0, 0], [0.4, 0, 0], [0.4, .13, 0], [0, .13, 0]]

    R, T = getMatrix(K, pixels, coordinates)
    drawRectangle(pixels, RED, image)
    newPixels = []

    for coordinate in coordinates:
        newPixels.append(getPixelPointFromRealWorldCordinates(K, R, T, coordinate))

    print('Recalculated points:')
    for pixel in newPixels:
        print(pixel)
    print('R ->', R)
    print('T ->', T)
    drawRectangle(newPixels, BLUE, image)
    img = cv2.imshow('image', image)
    cv2.waitKey(0)


