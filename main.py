from camera import K, R, T, getPixelPointFromRealWorldCordinates
import numpy as np
from calibration import getMatrix
SHOULD_PRINT = False


coordinates = [[0, 0, 0] , [0.4, 0, 0],[0, .13, 0],[0.4, .13, 0]]
pixels = []

for coordinate in coordinates:
	pixels.append(getPixelPointFromRealWorldCordinates(K,R,T,coordinate))
if SHOULD_PRINT:
	for pixel in pixels:
		print (pixel)
	print("R ->" , R)
	print("T ->" , T)

R, T = getMatrix(K,pixels, coordinates)

coordinates = [[0, 0, 0] , [0.4, 0, 0],[0, .13, 0],[0.4, .13, 0]]
pixels = []

for coordinate in coordinates:
	pixels.append(getPixelPointFromRealWorldCordinates(K,R,T,coordinate))
if SHOULD_PRINT:
	for pixel in pixels:
		print (pixel)
	print("R ->" , R)
	print("T ->" , T)
