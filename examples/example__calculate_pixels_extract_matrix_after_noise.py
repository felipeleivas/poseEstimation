from math import pi

import numpy as np

from calibration import getMatrix
from camera import getPixelPointFromRealWorldCordinates
from rotationMatrix import getRotationMatrix
from util import noisePixels
SHOULD_PRINT = True
ALPHA = pi / 2
BETA = 0
GAMA = 0


K = np.array([[1.0, 0, 0.0],
			  [0, 1.0, 0.0],
			  [0, 0, 1/64]])
R = getRotationMatrix(ALPHA, BETA, GAMA)
T = np.array([[3.7],[8],[0.5]])

coordinates = [[0, 0, 0], [0.4, 0, 0], [0, .13, 0], [0.4, .13, 0]]

pixels = []
for coordinate in coordinates:
    pixels.append(getPixelPointFromRealWorldCordinates(K, R, T, coordinate))
if SHOULD_PRINT:
    # for pixel in pixels:
    #     print(pixel)
    print('Original T ->', T)

for i in range(0, 5):
    newPixels = noisePixels(pixels, 0.05)
    coordinates = [[0, 0, 0], [0.4, 0, 0], [0, .13, 0], [0.4, .13, 0]]
    R, T = getMatrix(K, newPixels, coordinates)

    newPixels = []

    for coordinate in coordinates:
        newPixels.append(getPixelPointFromRealWorldCordinates(K, R, T, coordinate))
    if SHOULD_PRINT:
        # for pixel in newPixels:
        #     print(pixel)
        print('Estimated T ->', T)


