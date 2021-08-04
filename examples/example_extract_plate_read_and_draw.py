import cv2

import plate_detectation.example_plate_detection as test
from calibration import getMatrix
from camera import K, getPixelPointFromRealWorldCordinates
from util import *

coordinates = [[0, 0, 0], [0.4, 0, 0], [0.4, .13, 0], [0, .13, 0]]


def read_plate_pixels(filename):
    file = open('../points/pointFiles.csv', 'r')
    pixels = []
    for line in file:
        tokens = line.replace('\n', '').split(',')
        if tokens[0] == filename:
            for index in range(1, len(tokens) - 1, 2):
                pixels.append([float(tokens[index]), float(tokens[index + 1])])
            break
    return pixels


if __name__ == '__main__':
    imagePath = 'medias/carro_2_metros0.jpg'
    image = cv2.imread(imagePath)
    pixels = read_plate_pixels(imagePath)
    print('\n\n\n\n\n')

    print('Extracted points:')
    for pixel in pixels:
        print(pixel)

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
