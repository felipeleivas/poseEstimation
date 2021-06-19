from camera import K, R, T, getPixelPointFromRealWorldCordinates
import numpy as np
from calibration import getMatrix
from util import noisePixels
SHOULD_PRINT = True


coordinates = [[0, 0, 0] , [0.4, 0, 0],[0, .13, 0],[0.4, .13, 0]]
pixels = []

for coordinate in coordinates:
	pixels.append(getPixelPointFromRealWorldCordinates(K,R,T,coordinate))
if SHOULD_PRINT:
	for pixel in pixels:
		print (pixel)
	print("R ->" , R)
	print("T ->" , T)


	print("\n\n\n\n\n")
for i in range(0,1):
	newPixels = pixels
	# newPixels = noisePixels(pixels)
	coordinates = [[0, 0, 0] , [0.4, 0, 0],[0, .13, 0],[0.4, .13, 0]]

	print(newPixels)
	R, T = getMatrix(K,newPixels, coordinates)
	
	newPixels = []

	for coordinate in coordinates:
		newPixels.append(getPixelPointFromRealWorldCordinates(K,R,T,coordinate))
	if SHOULD_PRINT:
		for pixel in newPixels:
			print (pixel)
		print("R ->" , R)
		print("T ->" , T)

		print("\n\n\n\n\n")
